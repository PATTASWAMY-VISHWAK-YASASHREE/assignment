from __future__ import annotations

import pickle
from dataclasses import dataclass
from threading import RLock
from typing import Any, Dict, List, Optional, Tuple
from uuid import uuid4

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler, MinMaxScaler
from sklearn.tree import DecisionTreeClassifier

from app.schemas.pipeline import (
    PipelineRunRequest,
    PipelineRunResponse,
    PredictResponse,
    ConfusionMatrix,
    FeatureImportance,
    ModelType,
    PreprocessType,
)
from app.services import dataset_service


@dataclass
class TrainedModelArtifact:
    model: Any
    feature_columns: List[str]
    numeric_fill: Dict[str, Any]
    categorical_fill: Dict[str, Any]
    preprocessors: List[Tuple[str, List[str], Any]]
    ohe_columns: List[str]
    label_encoder: Optional[LabelEncoder]
    model_type: ModelType
    target_labels: List[Any]


_model_store: Dict[str, TrainedModelArtifact] = {}
_model_lock = RLock()


async def run_pipeline(request: PipelineRunRequest) -> PipelineRunResponse:
    df = dataset_service.get_dataset(request.dataset_id)
    warnings: List[str] = []

    if request.target_column not in df.columns:
        raise ValueError("Target column not found in dataset.")

    feature_cols = request.feature_columns or [c for c in df.columns if c != request.target_column]
    if len(feature_cols) == 0:
        raise ValueError("No feature columns selected.")

    df_features = df[feature_cols].copy()
    target = df[request.target_column]

    # Basic imputations
    numeric_fill: Dict[str, Any] = {}
    categorical_fill: Dict[str, Any] = {}

    for col in df_features.columns:
        if pd.api.types.is_numeric_dtype(df_features[col]):
            fill_value = df_features[col].median()
            numeric_fill[col] = fill_value
            df_features[col] = df_features[col].fillna(fill_value)
        else:
            fill_value = df_features[col].mode().iloc[0]
            categorical_fill[col] = fill_value
            df_features[col] = df_features[col].fillna(fill_value)
    if target.isna().any():
        fill_value = target.mode().iloc[0]
        target = target.fillna(fill_value)
        warnings.append(f"Missing target values filled with mode: {fill_value}.")

    numeric_cols = [c for c in df_features.columns if pd.api.types.is_numeric_dtype(df_features[c])]

    # Apply preprocessing steps on numeric columns
    preprocessors: List[Tuple[str, List[str], Any]] = []
    for step in request.preprocess:
        cols_to_scale: List[str]
        if step.columns:
            cols_to_scale = [c for c in step.columns if c in numeric_cols]
            missing_cols = set(step.columns) - set(cols_to_scale)
            if missing_cols:
                warnings.append(
                    f"Skipped non-numeric or missing columns for {step.step}: {', '.join(missing_cols)}"
                )
        else:
            cols_to_scale = numeric_cols

        if not cols_to_scale:
            continue

        scaler = StandardScaler() if step.step == PreprocessType.standardize else MinMaxScaler()
        df_features[cols_to_scale] = scaler.fit_transform(df_features[cols_to_scale])
        preprocessors.append((step.step.value, cols_to_scale, scaler))

    # One-hot encode remaining categorical columns
    df_features = pd.get_dummies(df_features, drop_first=False)
    ohe_columns = list(df_features.columns)

    # Encode target if needed
    label_encoder: Optional[LabelEncoder] = None
    if not pd.api.types.is_numeric_dtype(target):
        label_encoder = LabelEncoder()
        target = label_encoder.fit_transform(target)

    # Guard against rare classes
    unique, counts = np.unique(target, return_counts=True)
    rare = {cls: int(cnt) for cls, cnt in zip(unique, counts) if cnt < 2}
    if rare:
        if request.drop_rare_classes:
            mask = ~pd.Series(target).isin(list(rare.keys()))
            df_features = df_features.loc[mask].reset_index(drop=True)
            target = target[mask]
            warnings.append(
                "Dropped classes with <2 samples: " + ", ".join(str(k) for k in rare.keys())
            )
            # re-check after drop
            unique, counts = np.unique(target, return_counts=True)
            if len(unique) < 2:
                warnings.append(
                    "Insufficient classes after dropping rare classes; skipping model training."
                )
                return PipelineRunResponse(
                    status="success",
                    accuracy=None,
                    model_type=request.model,
                    confusion_matrix=None,
                    feature_importances=None,
                    warnings=warnings,
                )
        else:
            cls_list = ", ".join([f"{cls} ({cnt})" for cls, cnt in rare.items()])
            raise ValueError(
                "The least populated classes have fewer than 2 samples. "
                f"Classes with too few members: {cls_list}. Enable drop_rare_classes to filter them."
            )

    X_train, X_test, y_train, y_test = train_test_split(
        df_features,
        target,
        test_size=request.split.test_size,
        random_state=request.split.random_state,
        stratify=target if len(np.unique(target)) > 1 else None,
    )

    model = _build_model(request.model)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    acc = float(accuracy_score(y_test, y_pred))

    labels = label_encoder.classes_.tolist() if label_encoder else sorted(list(set(target)))
    cm = confusion_matrix(y_test, y_pred, labels=range(len(labels)))
    cm_matrix = cm.tolist()

    feature_importances = _extract_feature_importance(model, df_features.columns)

    artifact = TrainedModelArtifact(
        model=model,
        feature_columns=feature_cols,
        numeric_fill=numeric_fill,
        categorical_fill=categorical_fill,
        preprocessors=preprocessors,
        ohe_columns=ohe_columns,
        label_encoder=label_encoder,
        model_type=request.model,
        target_labels=labels,
    )
    model_id = _save_model(artifact)
    download_path = f"/api/pipeline/model/{model_id}/download"

    return PipelineRunResponse(
        status="success",
        accuracy=acc,
        model_type=request.model,
        confusion_matrix=ConfusionMatrix(labels=labels, matrix=cm_matrix),
        feature_importances=feature_importances,
        warnings=warnings,
        model_id=model_id,
        model_download_path=download_path,
    )


async def predict(model_id: str, records: List[Dict[str, Any]]) -> PredictResponse:
    artifact = _get_model(model_id)
    if not records:
        raise ValueError("Provide at least one record to predict.")

    df = pd.DataFrame(records)
    missing = [c for c in artifact.feature_columns if c not in df.columns]
    if missing:
        raise ValueError(f"Missing feature columns: {', '.join(missing)}")

    df_features = df[artifact.feature_columns].copy()

    for col, fill_value in artifact.numeric_fill.items():
        if col in df_features.columns:
            df_features[col] = df_features[col].fillna(fill_value)
    for col, fill_value in artifact.categorical_fill.items():
        if col in df_features.columns:
            df_features[col] = df_features[col].fillna(fill_value)

    for _, cols, scaler in artifact.preprocessors:
        cols_to_scale = [c for c in cols if c in df_features.columns]
        if cols_to_scale:
            df_features[cols_to_scale] = scaler.transform(df_features[cols_to_scale])

    df_features = pd.get_dummies(df_features, drop_first=False)
    df_features = df_features.reindex(columns=artifact.ohe_columns, fill_value=0)

    preds = artifact.model.predict(df_features)
    if artifact.label_encoder:
        preds = artifact.label_encoder.inverse_transform(preds)

    return PredictResponse(predictions=[_convert_pred(v) for v in preds])


def download_model_bytes(model_id: str) -> bytes:
    artifact = _get_model(model_id)
    return pickle.dumps(artifact)


def _build_model(model_type: ModelType):
    if model_type == ModelType.logistic_regression:
        return LogisticRegression(max_iter=1000, solver="lbfgs")
    if model_type == ModelType.decision_tree:
        return DecisionTreeClassifier(random_state=42)
    raise ValueError("Unsupported model type")


def _extract_feature_importance(model, feature_names: List[str]):
    importances: List[FeatureImportance] = []
    if hasattr(model, "feature_importances_"):
        scores = model.feature_importances_
    elif hasattr(model, "coef_"):
        coefs = getattr(model, "coef_")
        if len(coefs.shape) == 1:
            scores = np.abs(coefs)
        else:
            scores = np.mean(np.abs(coefs), axis=0)
    else:
        return None

    for name, score in zip(feature_names, scores):
        importances.append(FeatureImportance(name=name, importance=float(score)))

    # sort and keep top 15
    importances = sorted(importances, key=lambda x: x.importance, reverse=True)
    return importances[:15]


def _save_model(artifact: TrainedModelArtifact) -> str:
    model_id = str(uuid4())
    with _model_lock:
        _model_store[model_id] = artifact
    return model_id


def _get_model(model_id: str) -> TrainedModelArtifact:
    with _model_lock:
        if model_id not in _model_store:
            raise ValueError("Model not found. Please re-run the pipeline.")
        return _model_store[model_id]


def _convert_pred(value: Any) -> Any:
    if isinstance(value, (np.generic,)):
        return value.item()
    return value


def _clear_model_store():  # pragma: no cover - test helper
    with _model_lock:
        _model_store.clear()
