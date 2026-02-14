import { useState } from "react";
import {
  Alert,
  Box,
  Button,
  Card,
  CardContent,
  CardHeader,
  CircularProgress,
  LinearProgress,
  FormControlLabel,
  Stack,
  Switch,
  Tooltip,
  Typography,
} from "@mui/material";
import PlayArrowIcon from "@mui/icons-material/PlayArrow";
import CloudDownloadIcon from "@mui/icons-material/CloudDownload";

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
        drop_rare_classes: store.dropRareClasses,
      };

      const { data } = await api.post<PipelineRunResponse>("/pipeline/run", payload);
      store.setResult(data);
    } catch (err: unknown) {
      const detail = (err as { response?: { data?: { detail?: string } } })?.response?.data?.detail;
      setError(detail || "Pipeline failed");
      store.setResult(undefined);
    } finally {
      store.setRunning(false);
    }
  };

  return (
    <Card sx={{ height: "100%", minHeight: 320 }}>
      <CardHeader title="6. Run Pipeline" subheader="Execute the configured workflow" />
      <CardContent>
        <Stack spacing={2}>
          {store.running && (
            <Box>
              <Typography variant="body2" color="text.secondary" gutterBottom>
                Training in progress… powering up the model ⚡
              </Typography>
              <LinearProgress />
            </Box>
          )}
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
            {store.result?.model_download_path && (
              <Button
                variant="outlined"
                color="secondary"
                startIcon={<CloudDownloadIcon />}
                href={`${window.location.origin}${store.result.model_download_path}`}
              >
                Download model
              </Button>
            )}
          </Box>
          <Tooltip
            placement="right"
            title="If your target has classes with only one sample, enable this to drop them instead of failing."
          >
            <FormControlLabel
              control={
                <Switch
                  checked={store.dropRareClasses}
                  onChange={(e) => store.setDropRareClasses(e.target.checked)}
                  color="primary"
                />
              }
              label="Drop rare classes (≤1 sample)"
            />
          </Tooltip>
          {store.result?.warnings?.length ? (
            <Alert severity="warning">
              {store.result.warnings.map((w, idx) => (
                <div key={idx}>{w}</div>
              ))}
            </Alert>
          ) : null}
          {error?.toLowerCase().includes("least populated classes") ? (
            <Alert severity="info">
              Tip: Your target has classes with only one sample. Toggle "Drop rare classes" to automatically remove them and retry.
            </Alert>
          ) : null}
        </Stack>
      </CardContent>
    </Card>
  );
}
