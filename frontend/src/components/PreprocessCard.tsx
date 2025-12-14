import { useMemo, useState } from "react";
import {
  Box,
  Button,
  Card,
  CardContent,
  CardHeader,
  Chip,
  Divider,
  FormControl,
  InputLabel,
  MenuItem,
  OutlinedInput,
  Select,
  Stack,
  Typography,
} from "@mui/material";
import AddIcon from "@mui/icons-material/Add";
import DeleteIcon from "@mui/icons-material/Delete";

import { usePipelineStore } from "../store/usePipelineStore";
import { PreprocessStep } from "../types";

const OPTIONS = [
  { label: "Standardization (StandardScaler)", value: "standardize" },
  { label: "Normalization (MinMaxScaler)", value: "normalize" },
] as const;

export default function PreprocessCard() {
  const dataset = usePipelineStore((s) => s.dataset);
  const steps = usePipelineStore((s) => s.preprocessSteps);
  const addStep = usePipelineStore((s) => s.addPreprocessStep);
  const removeStep = usePipelineStore((s) => s.removePreprocessStep);

  const [selectedStep, setSelectedStep] = useState<typeof OPTIONS[number]["value"]>("standardize");
  const [columns, setColumns] = useState<string[]>([]);

  const availableColumns = useMemo(() => dataset?.column_names || [], [dataset]);

  const onAdd = () => {
    const payload: PreprocessStep = {
      step: selectedStep,
      columns: columns.length ? columns : undefined,
    } as PreprocessStep;
    addStep(payload);
    setColumns([]);
  };

  return (
    <Card sx={{ height: "100%", minHeight: 320 }}>
      <CardHeader title="3. Preprocessing" subheader="Add scaling steps to numeric columns" />
      <CardContent>
        {!dataset ? (
          <Box bgcolor="#fafafa" p={2} borderRadius={2}>
            <Typography color="text.secondary" gutterBottom>
              Upload a dataset to configure preprocessing. You'll be able to target specific numeric columns or all of them.
            </Typography>
            <Button variant="outlined" size="small" disabled>
              Add step
            </Button>
          </Box>
        ) : (
          <>
            <Stack spacing={2} direction={{ xs: "column", md: "row" }} alignItems="center">
              <FormControl fullWidth>
                <InputLabel id="preprocess-type">Step</InputLabel>
                <Select
                  labelId="preprocess-type"
                  value={selectedStep}
                  label="Step"
                  onChange={(e) => setSelectedStep(e.target.value as any)}
                >
                  {OPTIONS.map((opt) => (
                    <MenuItem key={opt.value} value={opt.value}>
                      {opt.label}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>

              <FormControl fullWidth>
                <InputLabel id="preprocess-cols">Columns (optional)</InputLabel>
                <Select
                  multiple
                  labelId="preprocess-cols"
                  value={columns}
                  onChange={(e) => setColumns(e.target.value as string[])}
                  input={<OutlinedInput label="Columns" />}
                  renderValue={(selected) => (
                    <Stack direction="row" spacing={1} flexWrap="wrap">
                      {selected.map((value) => (
                        <Chip key={value} label={value} />
                      ))}
                    </Stack>
                  )}
                >
                  {availableColumns.map((col) => (
                    <MenuItem key={col} value={col}>
                      {col}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>

              <Button variant="contained" startIcon={<AddIcon />} onClick={onAdd}>
                Add
              </Button>
            </Stack>

            <Divider sx={{ my: 2 }} />
            {steps.length === 0 ? (
              <Typography variant="body2" color="text.secondary">
                No preprocessing steps added yet.
              </Typography>
            ) : (
              <Stack spacing={1}>
                {steps.map((s, idx) => (
                  <Box
                    key={`${s.step}-${idx}`}
                    display="flex"
                    alignItems="center"
                    justifyContent="space-between"
                    p={1.2}
                    borderRadius={1}
                    bgcolor="#f7f7fb"
                  >
                    <Typography variant="subtitle2">
                      {s.step === "standardize" ? "Standardization" : "Normalization"}
                    </Typography>
                    <Stack direction="row" spacing={1} alignItems="center">
                      {s.columns?.length ? (
                        <Stack direction="row" spacing={0.5} flexWrap="wrap">
                          {s.columns.map((c) => (
                            <Chip key={c} size="small" label={c} />
                          ))}
                        </Stack>
                      ) : (
                        <Typography variant="caption" color="text.secondary">
                          All numeric columns
                        </Typography>
                      )}
                      <Button color="error" startIcon={<DeleteIcon />} onClick={() => removeStep(idx)}>
                        Remove
                      </Button>
                    </Stack>
                  </Box>
                ))}
              </Stack>
            )}
          </>
        )}
      </CardContent>
    </Card>
  );
}
