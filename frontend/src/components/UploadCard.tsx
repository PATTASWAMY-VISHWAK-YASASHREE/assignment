import { ChangeEvent, useState } from "react";
import { Box, Button, Card, CardContent, CardHeader, LinearProgress, Typography } from "@mui/material";
import CloudUploadIcon from "@mui/icons-material/CloudUpload";

import api from "../api";
import { DatasetUploadResponse } from "../types";
import { usePipelineStore } from "../store/usePipelineStore";

const ACCEPTED = ".csv,.xlsx";

export default function UploadCard() {
  const setDataset = usePipelineStore((s) => s.setDataset);
  const reset = usePipelineStore((s) => s.reset);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleFile = async (e: ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    setError(null);
    setLoading(true);
    try {
      const formData = new FormData();
      formData.append("file", file);
      const { data } = await api.post<DatasetUploadResponse>("/datasets/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      reset();
      setDataset(data);
    } catch (err: any) {
      setError(err?.response?.data?.detail || "Failed to upload file");
    } finally {
      setLoading(false);
      e.target.value = "";
    }
  };

  return (
    <Card>
      <CardHeader title="1. Upload Dataset" subheader="Upload CSV or Excel to get started" />
      <CardContent>
        <Box display="flex" gap={2} alignItems="center" flexWrap="wrap">
          <Button component="label" variant="contained" startIcon={<CloudUploadIcon />} disabled={loading}>
            Select File
            <input hidden type="file" accept={ACCEPTED} onChange={handleFile} />
          </Button>
          {loading && <LinearProgress sx={{ minWidth: 200 }} />}
          {error && (
            <Typography color="error" variant="body2">
              {error}
            </Typography>
          )}
        </Box>
        <Typography variant="caption" color="text.secondary" display="block" mt={1}>
          Accepted: {ACCEPTED}
        </Typography>
      </CardContent>
    </Card>
  );
}
