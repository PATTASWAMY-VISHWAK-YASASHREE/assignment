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

  const marks = [
    { value: 10, label: "10%" },
    { value: 20, label: "20%" },
    { value: 30, label: "30%" },
    { value: 40, label: "40%" },
    { value: 50, label: "50%" },
  ];

  return (
    <Card sx={{ height: "100%", minHeight: 320 }}>
      <CardHeader title="4. Train / Test Split" subheader="Pick how much data is used for testing" />
      <CardContent>
        <Stack spacing={2}>
          <Slider
            value={testPercent}
            onChange={handleChange}
            step={5}
            min={10}
            max={50}
            valueLabelDisplay="auto"
            marks={marks}
            aria-label="Test set percentage"
            getAriaValueText={(value) => `Test set: ${value}%`}
            valueLabelFormat={(value) => `${value}%`}
          />
          <Typography variant="body2" color="text.secondary">
            Train: {trainPercent}% • Test: {testPercent}%
          </Typography>
        </Stack>
      </CardContent>
    </Card>
  );
}
