import { useState } from "react";
import {
  Alert,
  Box,
  Button,
  Card,
  CardContent,
  CardHeader,
  CircularProgress,
  Stack,
  TextField,
  Typography,
} from "@mui/material";
import SmartToyIcon from "@mui/icons-material/SmartToy";

import api from "../api";
import { PredictResponse } from "../types";
import { usePipelineStore } from "../store/usePipelineStore";

const sampleInput = `{
  "feature1": 1,
  "feature2": 0.2
}`;

export default function PlaygroundCard() {
  const store = usePipelineStore();
  const [rawInput, setRawInput] = useState(sampleInput);
  const [predictions, setPredictions] = useState<Array<string | number>>([]);
  const [error, setError] = useState<string | null>(null);
  const [jsonError, setJsonError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const validateJson = () => {
    try {
      JSON.parse(rawInput);
      setJsonError(null);
      return true;
    } catch (err) {
      setJsonError("Invalid JSON format.");
      return false;
    }
  };

  const onPredict = async () => {
    setError(null);
    setPredictions([]);

    if (!store.result?.model_id) {
      setError("Run a pipeline first to produce a model.");
      return;
    }

    if (!validateJson()) return;

    let records: Array<Record<string, unknown>> = [];
    try {
      const parsed = JSON.parse(rawInput);
      records = Array.isArray(parsed) ? parsed : [parsed];
    } catch (err) {
      setError("Invalid JSON. Provide one record or an array of records.");
      return;
    }

    setLoading(true);
    try {
      const { data } = await api.post<PredictResponse>("/pipeline/predict", {
        model_id: store.result.model_id,
        records,
      });
      setPredictions(data.predictions);
    } catch (err: any) {
      setError(err?.response?.data?.detail || "Prediction failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card sx={{ height: "100%", minHeight: 280 }}>
      <CardHeader title="Playground" subheader="Send ad-hoc records to the trained model" />
      <CardContent>
        <Stack spacing={2}>
          {!store.result?.model_id && (
            <Alert severity="info">Run the pipeline to enable predictions and downloads.</Alert>
          )}

          <TextField
            label="JSON input"
            value={rawInput}
            onChange={(e) => {
              setRawInput(e.target.value);
              if (jsonError) setJsonError(null);
            }}
            onBlur={() => validateJson()}
            error={!!jsonError}
            minRows={6}
            multiline
            fullWidth
            helperText={
              jsonError ||
              "Provide either a single JSON object or an array of objects with the selected feature columns."
            }
            sx={{ "& .MuiInputBase-input": { fontFamily: "monospace" } }}
          />

          <Box display="flex" gap={2} alignItems="center">
            <Button
              variant="contained"
              startIcon={loading ? <CircularProgress size={18} color="inherit" /> : <SmartToyIcon />}
              onClick={onPredict}
              disabled={loading || !store.result?.model_id}
            >
              {loading ? "Predicting..." : "Send to model"}
            </Button>
            {predictions.length > 0 && (
              <Box role="status" aria-live="polite">
                <Typography color="secondary" fontWeight={600}>
                  Predictions: {predictions.map((p) => String(p)).join(", ")}
                </Typography>
              </Box>
            )}
          </Box>

          {error && <Alert severity="error">{error}</Alert>}
        </Stack>
      </CardContent>
    </Card>
  );
}
