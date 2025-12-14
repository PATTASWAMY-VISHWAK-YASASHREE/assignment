import { create } from "zustand";
import { persist, createJSONStorage } from "zustand/middleware";
import { DatasetUploadResponse, ModelType, PipelineRunResponse, PreprocessStep, TrainTestConfig } from "../types";

export type PipelineState = {
  dataset?: DatasetUploadResponse;
  targetColumn?: string;
  featureColumns?: string[];
  preprocessSteps: PreprocessStep[];
  split: TrainTestConfig;
  model?: ModelType;
  dropRareClasses: boolean;
  running: boolean;
  result?: PipelineRunResponse;
  setDataset: (dataset: DatasetUploadResponse) => void;
  setTargetColumn: (col?: string) => void;
  setFeatureColumns: (cols?: string[]) => void;
  addPreprocessStep: (step: PreprocessStep) => void;
  removePreprocessStep: (index: number) => void;
  setSplit: (split: TrainTestConfig) => void;
  setModel: (model: ModelType) => void;
  setDropRareClasses: (drop: boolean) => void;
  setRunning: (running: boolean) => void;
  setResult: (result?: PipelineRunResponse) => void;
  reset: () => void;
};

export const usePipelineStore = create<PipelineState>()(
  persist(
    (set) => ({
      preprocessSteps: [],
      split: { test_size: 0.2, random_state: 42 },
      dropRareClasses: false,
      running: false,
      setDataset: (dataset) =>
        set(() => {
          const cols = dataset.column_names || [];
          const targetColumn = cols.length ? cols[0] : undefined;
          const featureColumns = cols.length > 1 ? cols.slice(1) : undefined;
          return { dataset, targetColumn, featureColumns };
        }),
      setTargetColumn: (col) => set({ targetColumn: col }),
      setFeatureColumns: (cols) => set({ featureColumns: cols }),
      addPreprocessStep: (step) => set((state) => ({ preprocessSteps: [...state.preprocessSteps, step] })),
      removePreprocessStep: (index) =>
        set((state) => ({ preprocessSteps: state.preprocessSteps.filter((_, i) => i !== index) })),
      setSplit: (split) => set({ split }),
      setModel: (model) => set({ model }),
      setDropRareClasses: (drop) => set({ dropRareClasses: drop }),
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
          dropRareClasses: false,
          running: false,
          result: undefined,
        }),
    }),
    {
      name: "pipeline-store",
      storage: createJSONStorage(() => localStorage),
      partialize: (state) => ({
        dataset: state.dataset,
        targetColumn: state.targetColumn,
        featureColumns: state.featureColumns,
        preprocessSteps: state.preprocessSteps,
        split: state.split,
        model: state.model,
        dropRareClasses: state.dropRareClasses,
        result: state.result,
      }),
    }
  )
);
