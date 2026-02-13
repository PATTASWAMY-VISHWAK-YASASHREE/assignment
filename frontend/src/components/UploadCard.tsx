import { ChangeEvent, useState, DragEvent } from "react";
import { Box, Button, Card, CardContent, CardHeader, LinearProgress, Typography, alpha } from "@mui/material";
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
  const [isDragActive, setIsDragActive] = useState(false);

  const uploadFile = async (file: File) => {
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
    }
  };

  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      uploadFile(file);
    }
    e.target.value = "";
  };

  const handleDragOver = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    if (loading) return;
    setIsDragActive(true);
  };

  const handleDragLeave = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragActive(false);
  };

  const handleDrop = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragActive(false);

    if (loading) return;

    const file = e.dataTransfer.files?.[0];
    if (file) {
      uploadFile(file);
    }
  };

  return (
    <Card sx={{ height: "100%", minHeight: 320 }}>
      <CardHeader title="1. Upload Dataset" subheader="Upload CSV or Excel to get started" />
      <CardContent>
        <Box
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          sx={{
            border: "2px dashed",
            borderColor: isDragActive ? "primary.main" : "divider",
            borderRadius: 2,
            p: 3,
            bgcolor: isDragActive ? (theme) => alpha(theme.palette.primary.main, 0.05) : "transparent",
            transition: "all 0.2s",
            textAlign: "center",
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            gap: 2,
            minHeight: 200,
            justifyContent: "center"
          }}
        >
          <CloudUploadIcon sx={{ fontSize: 48, color: isDragActive ? "primary.main" : "text.secondary" }} />

          <Box>
            <Typography variant="body1" gutterBottom fontWeight={500}>
              Drag and drop your file here
            </Typography>
            <Typography variant="body2" color="text.secondary" gutterBottom>
              or
            </Typography>
            <Button component="label" variant="contained" disabled={loading}>
              Select File
              <input hidden type="file" accept={ACCEPTED} onChange={handleFileChange} />
            </Button>
          </Box>

          {loading && <LinearProgress sx={{ width: "100%", maxWidth: 300 }} />}

          {error && (
            <Typography color="error" variant="body2">
              {error}
            </Typography>
          )}

          <Typography variant="caption" color="text.secondary" display="block">
            Accepted: {ACCEPTED}
          </Typography>
        </Box>
      </CardContent>
    </Card>
  );
}
