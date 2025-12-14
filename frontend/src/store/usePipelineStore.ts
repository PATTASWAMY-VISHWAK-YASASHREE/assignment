import { create } from "zustand";
import { DatasetUploadResponse, ModelType, PipelineRunResponse, PreprocessStep, TrainTestConfig } from "../types";

export type PipelineState = {
  dataset?: DatasetUploadResponse;
  targetColumn?: string;
  featureColumns?: string[];
  preprocessSteps: PreprocessStep[];
  split: TrainTestConfig;
  model?: ModelType;
  running: boolean;
  result?: PipelineRunResponse;
  setDataset: (dataset: DatasetUploadResponse) => void;
  setTargetColumn: (col?: string) => void;
  setFeatureColumns: (cols?: string[]) => void;
  addPreprocessStep: (step: PreprocessStep) => void;
  removePreprocessStep: (index: number) => void;
  setSplit: (split: TrainTestConfig) => void;
  setModel: (model: ModelType) => void;
  setRunning: (running: boolean) => void;
  setResult: (result?: PipelineRunResponse) => void;
  reset: () => void;
};

export const usePipelineStore = create<PipelineState>((set) => ({
  preprocessSteps: [],
  split: { test_size: 0.2, random_state: 42 },
  running: false,
  setDataset: (dataset) => set({ dataset }),
  setTargetColumn: (col) => set({ targetColumn: col }),
  setFeatureColumns: (cols) => set({ featureColumns: cols }),
  addPreprocessStep: (step) => set((state) => ({ preprocessSteps: [...state.preprocessSteps, step] })),
  removePreprocessStep: (index) =>
    set((state) => ({ preprocessSteps: state.preprocessSteps.filter((_, i) => i !== index) })),
  setSplit: (split) => set({ split }),
  setModel: (model) => set({ model }),
  setRunning: (running) => set({ running }),
  setResult: (result) => set({ result }),
  reset: () =>
    set({
      dataset: undefined,
      targetColumn: undefined,
      featureColumns: undefined,
      preprocessSteps: [],
      split: { test_size: 0.2, random_state: 42 },
      model: undefined,
      running: false,
      result: undefined,
    }),
}));
