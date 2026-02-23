import { ChangeEvent, DragEvent, useRef, useState } from "react";
import { Alert, Box, Button, Card, CardContent, CardHeader, LinearProgress, Typography } from "@mui/material";
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
  const [success, setSuccess] = useState(false);
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const processFile = async (file: File) => {
    if (!file) return;
    setError(null);
    setSuccess(false);
    setLoading(true);
    try {
      const formData = new FormData();
      formData.append("file", file);
      const { data } = await api.post<DatasetUploadResponse>("/datasets/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      reset();
      setDataset(data);
      setSuccess(true);
      setTimeout(() => setSuccess(false), 3000);
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
          onClick={() => {
            if (!loading) fileInputRef.current?.click();
          }}
          onKeyDown={(e) => {
            if (e.key === "Enter" || e.key === " ") {
              e.preventDefault();
              if (!loading) fileInputRef.current?.click();
            }
          }}
          role="button"
          tabIndex={0}
          aria-label="Upload file area. Drag and drop a CSV or Excel file here, or click to select."
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
              outlineOffset: "2px",
            },
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

          <Button
            component="div"
            role="presentation"
            tabIndex={-1}
            variant="contained"
            disabled={loading}
            sx={{ pointerEvents: "none" }}
          >
            Select File
          </Button>
          <input
            ref={fileInputRef}
            hidden
            type="file"
            accept={ACCEPTED}
            onChange={handleFile}
          />

          <Box width="100%" maxWidth={300} aria-live="polite">
            {loading && (
              <Box aria-busy="true" mb={1}>
                <Typography variant="caption" display="block" gutterBottom>
                  Uploading...
                </Typography>
                <LinearProgress sx={{ width: "100%" }} />
              </Box>
            )}
            {error && (
              <Alert severity="error" sx={{ width: "100%", mt: 1 }}>
                {error}
              </Alert>
            )}
            {success && (
              <Alert severity="success" sx={{ width: "100%", mt: 1 }}>
                File uploaded successfully!
              </Alert>
            )}
          </Box>

          <Typography variant="caption" color="text.secondary" display="block">
            Accepted: {ACCEPTED}
          </Typography>
        </Box>
      </CardContent>
    </Card>
  );
}
