import { Card, CardContent, CardHeader, FormControlLabel, Radio, RadioGroup, Stack, Typography } from "@mui/material";

import { usePipelineStore } from "../store/usePipelineStore";

export default function ModelCard() {
  const model = usePipelineStore((s) => s.model);
  const setModel = usePipelineStore((s) => s.setModel);

  return (
    <Card>
      <CardHeader title="5. Choose Model" subheader="One model per run" />
      <CardContent>
        <RadioGroup value={model || ""} onChange={(e) => setModel(e.target.value as any)}>
          <FormControlLabel
            value="logistic_regression"
            control={<Radio />}
            label={
              <Stack>
                <Typography>Logistic Regression</Typography>
                <Typography variant="caption" color="text.secondary">
                  Baseline linear classifier with L2 regularization.
                </Typography>
              </Stack>
            }
          />
          <FormControlLabel
            value="decision_tree"
            control={<Radio />}
            label={
              <Stack>
                <Typography>Decision Tree Classifier</Typography>
                <Typography variant="caption" color="text.secondary">
                  Non-linear splits with built-in feature importance.
                </Typography>
              </Stack>
            }
          />
        </RadioGroup>
      </CardContent>
    </Card>
  );
}
