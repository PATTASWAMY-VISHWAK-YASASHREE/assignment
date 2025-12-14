from __future__ import annotations

from typing import List, Optional

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
    ConfusionMatrix,
    FeatureImportance,
    ModelType,
    PreprocessType,
)
from app.services import dataset_service


async def run_pipeline(request: PipelineRunRequest) -> PipelineRunResponse:
    df = dataset_service.get_dataset(request.dataset_id).copy()
    warnings: List[str] = []

    if request.target_column not in df.columns:
        raise ValueError("Target column not found in dataset.")

    feature_cols = request.feature_columns or [c for c in df.columns if c != request.target_column]
    if len(feature_cols) == 0:
        raise ValueError("No feature columns selected.")

    df_features = df[feature_cols].copy()
    target = df[request.target_column]

    # Basic imputations
    for col in df_features.columns:
        if pd.api.types.is_numeric_dtype(df_features[col]):
            df_features[col] = df_features[col].fillna(df_features[col].median())
        else:
            df_features[col] = df_features[col].fillna(df_features[col].mode().iloc[0])
    if target.isna().any():
        fill_value = target.mode().iloc[0]
        target = target.fillna(fill_value)
        warnings.append(f"Missing target values filled with mode: {fill_value}.")

    numeric_cols = [c for c in df_features.columns if pd.api.types.is_numeric_dtype(df_features[c])]

    # Apply preprocessing steps on numeric columns
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

    # One-hot encode remaining categorical columns
    df_features = pd.get_dummies(df_features, drop_first=False)

    # Encode target if needed
    label_encoder: Optional[LabelEncoder] = None
    if not pd.api.types.is_numeric_dtype(target):
        label_encoder = LabelEncoder()
        target = label_encoder.fit_transform(target)

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

    return PipelineRunResponse(
        status="success",
        accuracy=acc,
        model_type=request.model,
        confusion_matrix=ConfusionMatrix(labels=labels, matrix=cm_matrix),
        feature_importances=feature_importances,
        warnings=warnings,
    )


def _build_model(model_type: ModelType):
    if model_type == ModelType.logistic_regression:
        return LogisticRegression(max_iter=1000, n_jobs=-1)
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
