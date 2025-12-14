import {
  Card,
  CardContent,
  CardHeader,
  Chip,
  FormControl,
  InputLabel,
  MenuItem,
  OutlinedInput,
  Select,
  Stack,
  Typography,
  Table,
  TableHead,
  TableRow,
  TableCell,
  TableBody,
} from "@mui/material";

import { usePipelineStore } from "../store/usePipelineStore";

export default function DataOverview() {
  const dataset = usePipelineStore((s) => s.dataset);
  const targetColumn = usePipelineStore((s) => s.targetColumn);
  const featureColumns = usePipelineStore((s) => s.featureColumns);
  const setTargetColumn = usePipelineStore((s) => s.setTargetColumn);
  const setFeatureColumns = usePipelineStore((s) => s.setFeatureColumns);

  if (!dataset) return null;

  const columns = dataset.column_names;

  return (
    <Card>
      <CardHeader
        title="2. Inspect & Select Columns"
        subheader={`${dataset.rows.toLocaleString()} rows • ${dataset.columns} columns`}
      />
      <CardContent>
        <Stack direction={{ xs: "column", md: "row" }} spacing={2}>
          <FormControl fullWidth>
            <InputLabel id="target-label">Target column</InputLabel>
            <Select
              labelId="target-label"
              value={targetColumn || ""}
              label="Target column"
              onChange={(e) => setTargetColumn(e.target.value as string)}
            >
              {columns.map((col) => (
                <MenuItem key={col} value={col}>
                  {col}
                </MenuItem>
              ))}
            </Select>
          </FormControl>

          <FormControl fullWidth>
            <InputLabel id="feature-label">Feature columns (optional)</InputLabel>
            <Select
              multiple
              labelId="feature-label"
              value={featureColumns || []}
              onChange={(e) => setFeatureColumns(e.target.value as string[])}
              input={<OutlinedInput label="Feature columns" />}
              renderValue={(selected) => (
                <Stack direction="row" spacing={1} flexWrap="wrap">
                  {(selected as string[]).map((value) => (
                    <Chip key={value} label={value} />
                  ))}
                </Stack>
              )}
            >
              {columns
                .filter((c) => c !== targetColumn)
                .map((col) => (
                  <MenuItem key={col} value={col}>
                    {col}
                  </MenuItem>
                ))}
            </Select>
          </FormControl>
        </Stack>

        <Typography variant="subtitle2" mt={3} mb={1}>
          Preview (first 5 rows)
        </Typography>
        <Table size="small">
          <TableHead>
            <TableRow>
              {columns.map((col) => (
                <TableCell key={col}>{col}</TableCell>
              ))}
            </TableRow>
          </TableHead>
          <TableBody>
            {dataset.preview.map((row, idx) => (
              <TableRow key={idx}>
                {columns.map((col) => (
                  <TableCell key={col}>{String(row[col] ?? "")}</TableCell>
                ))}
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </CardContent>
    </Card>
  );
}
