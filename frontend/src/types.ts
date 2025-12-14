export type DatasetUploadResponse = {
  dataset_id: string;
  rows: number;
  columns: number;
  column_names: string[];
  dtypes: Record<string, string>;
  preview: Array<Record<string, unknown>>;
};

export type PreprocessStep = {
  step: "standardize" | "normalize";
  columns?: string[];
};

export type TrainTestConfig = {
  test_size: number;
  random_state?: number;
};

export type ModelType = "logistic_regression" | "decision_tree";

export type PipelineRunRequest = {
  dataset_id: string;
  target_column: string;
  feature_columns?: string[];
  preprocess: PreprocessStep[];
  split: TrainTestConfig;
  model: ModelType;
  drop_rare_classes?: boolean;
};

export type ConfusionMatrix = {
  labels: string[];
  matrix: number[][];
};

export type FeatureImportance = {
  name: string;
  importance: number;
};

export type PipelineRunResponse = {
  status: string;
  accuracy?: number;
  confusion_matrix?: ConfusionMatrix;
  feature_importances?: FeatureImportance[];
  message?: string;
  warnings?: string[];
  model_type?: ModelType;
  model_id?: string;
  model_download_path?: string;
};

export type PredictRequest = {
  model_id: string;
  records: Array<Record<string, unknown>>;
};

export type PredictResponse = {
  predictions: Array<string | number>;
};
