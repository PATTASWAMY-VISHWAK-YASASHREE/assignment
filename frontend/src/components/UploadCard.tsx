import { ChangeEvent, DragEvent, useState, useRef, KeyboardEvent } from "react";
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
  const inputRef = useRef<HTMLInputElement>(null);

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

  const handleKeyDown = (e: KeyboardEvent) => {
    if (e.key === "Enter" || e.key === " ") {
      e.preventDefault();
      inputRef.current?.click();
    }
  };

  return (
    <Card sx={{ height: "100%", minHeight: 320 }}>
      <CardHeader title="1. Upload Dataset" subheader="Upload CSV or Excel to get started" />
      <CardContent>
        <Box
          component="label"
          htmlFor="file-upload"
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
          tabIndex={0}
          role="button"
          aria-label="File upload dropzone. Drag and drop a file here or press Enter to select."
          onKeyDown={handleKeyDown}
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
            cursor: "pointer",
            "&:focus-visible": {
              outline: "2px solid",
              outlineColor: "primary.main",
              outlineOffset: 2,
            },
          }}
        >
          <input
            hidden
            id="file-upload"
            type="file"
            accept={ACCEPTED}
            onChange={handleFile}
            ref={inputRef}
          />
          <CloudUploadIcon
            sx={{ fontSize: 48, color: isDragging ? "primary.main" : "text.secondary", opacity: 0.5 }}
            aria-hidden="true"
          />
          <Box>
            <Typography variant="body1" gutterBottom fontWeight={500}>
              {isDragging ? "Drop file now" : "Drag & drop file here"}
            </Typography>
            <Typography variant="body2" color="text.secondary" gutterBottom>
              or click below to browse
            </Typography>
          </Box>
          <Button
            component="div"
            variant="contained"
            disabled={loading}
            tabIndex={-1}
            role="presentation"
            sx={{ pointerEvents: "none" }} // Ensure clicks pass through to label
          >
            Select File
          </Button>
          {loading && <LinearProgress sx={{ width: "100%", maxWidth: 300, mt: 1 }} />}
          {error && (
            <Typography color="error" variant="body2" role="alert">
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
