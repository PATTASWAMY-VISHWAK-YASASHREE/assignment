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

  const isMissingRequirements = !store.dataset || !store.targetColumn || !store.model;

  let disabledReason = "";
  if (!store.dataset) disabledReason = "Upload a dataset first.";
  else if (!store.targetColumn) disabledReason = "Select a target column.";
  else if (!store.model) disabledReason = "Choose a model to train.";
  else if (store.running) disabledReason = "Pipeline is running...";

  const isDisabled = store.running || isMissingRequirements;

  const run = async () => {
    setError(null);
    if (isMissingRequirements) {
      return;
    }

    store.setRunning(true);
    try {
      const payload = {
        dataset_id: store.dataset?.dataset_id,
        target_column: store.targetColumn,
        feature_columns: store.featureColumns,
        preprocess: store.preprocessSteps,
        split: store.split,
        model: store.model,
        drop_rare_classes: store.dropRareClasses,
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
            <Tooltip
              title={isDisabled ? disabledReason : ""}
              disableHoverListener={!isDisabled}
              disableFocusListener={!isDisabled}
              disableTouchListener={!isDisabled}
            >
              <span tabIndex={isDisabled ? 0 : undefined} style={{ display: "inline-flex" }}>
                <Button
                  variant="contained"
                  startIcon={store.running ? <CircularProgress size={18} color="inherit" /> : <PlayArrowIcon />}
                  onClick={run}
                  disabled={isDisabled}
                  sx={{ pointerEvents: isDisabled ? "none" : "auto" }}
                >
                  {store.running ? "Running..." : "Run Pipeline"}
                </Button>
              </span>
            </Tooltip>
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
