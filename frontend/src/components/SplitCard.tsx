import { Card, CardContent, CardHeader, Slider, Stack, Typography } from "@mui/material";

import { usePipelineStore } from "../store/usePipelineStore";

export default function SplitCard() {
  const split = usePipelineStore((s) => s.split);
  const setSplit = usePipelineStore((s) => s.setSplit);

  const handleChange = (_: Event, value: number | number[]) => {
    const val = Array.isArray(value) ? value[0] : value;
    const testSize = val / 100;
    setSplit({ ...split, test_size: testSize });
  };

  const testPercent = Math.round(split.test_size * 100);
  const trainPercent = 100 - testPercent;

  return (
    <Card>
      <CardHeader title="4. Train / Test Split" subheader="Pick how much data is used for testing" />
      <CardContent>
        <Stack spacing={2}>
          <Slider value={testPercent} onChange={handleChange} step={5} min={10} max={50} valueLabelDisplay="auto" />
          <Typography variant="body2" color="text.secondary">
            Train: {trainPercent}% • Test: {testPercent}%
          </Typography>
        </Stack>
      </CardContent>
    </Card>
  );
}
