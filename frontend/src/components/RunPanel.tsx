import { useState } from "react";
import { Alert, Box, Button, Card, CardContent, CardHeader, CircularProgress, Stack, Typography } from "@mui/material";
import PlayArrowIcon from "@mui/icons-material/PlayArrow";

import api from "../api";
import { PipelineRunResponse } from "../types";
import { usePipelineStore } from "../store/usePipelineStore";

export default function RunPanel() {
  const store = usePipelineStore();
  const [error, setError] = useState<string | null>(null);

  const run = async () => {
    setError(null);
    if (!store.dataset) {
      setError("Upload a dataset first.");
      return;
    }
    if (!store.targetColumn) {
      setError("Select a target column.");
      return;
    }
    if (!store.model) {
      setError("Choose a model to train.");
      return;
    }

    store.setRunning(true);
    try {
      const payload = {
        dataset_id: store.dataset.dataset_id,
        target_column: store.targetColumn,
        feature_columns: store.featureColumns,
        preprocess: store.preprocessSteps,
        split: store.split,
        model: store.model,
      };

      const { data } = await api.post<PipelineRunResponse>("/pipeline/run", payload);
      store.setResult(data);
    } catch (err: any) {
      setError(err?.response?.data?.detail || "Pipeline failed");
      store.setResult(undefined);
    } finally {
      store.setRunning(false);
    }
  };

  return (
    <Card>
      <CardHeader title="6. Run Pipeline" subheader="Execute the configured workflow" />
      <CardContent>
        <Stack spacing={2}>
          {error && <Alert severity="error">{error}</Alert>}
          <Box display="flex" alignItems="center" gap={2}>
            <Button
              variant="contained"
              startIcon={store.running ? <CircularProgress size={18} color="inherit" /> : <PlayArrowIcon />}
              onClick={run}
              disabled={store.running}
            >
              {store.running ? "Running..." : "Run Pipeline"}
            </Button>
            {store.result && (
              <Typography color="secondary" fontWeight={600}>
                Accuracy: {(store.result.accuracy ?? 0).toFixed(3)}
              </Typography>
            )}
          </Box>
          {store.result?.warnings?.length ? (
            <Alert severity="warning">
              {store.result.warnings.map((w, idx) => (
                <div key={idx}>{w}</div>
              ))}
            </Alert>
          ) : null}
        </Stack>
      </CardContent>
    </Card>
  );
}
