import { ChangeEvent, DragEvent, useState } from "react";
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
  const [isDragging, setIsDragging] = useState(false);

  const processFile = async (file: File) => {
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
    }
  };

  const handleFile = (e: ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) processFile(file);
    e.target.value = "";
  };

  const onDrop = (e: DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    if (loading) return;
    const file = e.dataTransfer.files?.[0];
    if (file) processFile(file);
  };

  return (
    <Card sx={{ height: "100%", minHeight: 320 }}>
      <CardHeader title="1. Upload Dataset" subheader="Upload CSV or Excel to get started" />
      <CardContent>
        <Box
          onDragOver={(e) => {
            e.preventDefault();
            if (!loading) setIsDragging(true);
          }}
          onDragLeave={(e) => {
            if (!e.currentTarget.contains(e.relatedTarget as Node)) {
              setIsDragging(false);
            }
          }}
          onDrop={onDrop}
          sx={{
            border: "2px dashed",
            borderColor: isDragging ? "primary.main" : "divider",
            borderRadius: 2,
            p: 4,
            textAlign: "center",
            bgcolor: isDragging ? "action.hover" : "background.paper",
            transition: "all 0.2s",
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            gap: 2,
          }}
        >
          <CloudUploadIcon
            sx={{ fontSize: 48, color: isDragging ? "primary.main" : "text.secondary", opacity: 0.5 }}
          />
          <Box>
            <Typography variant="body1" gutterBottom fontWeight={500}>
              {isDragging ? "Drop file now" : "Drag & drop file here"}
            </Typography>
            <Typography variant="body2" color="text.secondary" gutterBottom>
              or click below to browse
            </Typography>
          </Box>
          <Button component="label" variant="contained" disabled={loading}>
            Select File
            <input hidden type="file" accept={ACCEPTED} onChange={handleFile} />
          </Button>
          {loading && <LinearProgress sx={{ width: "100%", maxWidth: 300, mt: 1 }} />}
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
