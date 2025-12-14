import { Card, CardContent, CardHeader, Grid, Stack, Typography } from "@mui/material";

import { usePipelineStore } from "../store/usePipelineStore";
import FeatureImportanceChart from "./FeatureImportanceChart";
import { ConfusionMatrix } from "./ConfusionMatrix";

export default function ResultsPanel() {
  const result = usePipelineStore((s) => s.result);

  if (!result) return null;

  return (
    <Card>
      <CardHeader title="7. Results" />
      <CardContent>
        <Stack spacing={2}>
          <Typography variant="h6">Accuracy: {(result.accuracy ?? 0).toFixed(3)}</Typography>
          <Grid container spacing={2}>
            {result.confusion_matrix && (
              <Grid item xs={12} md={6}>
                <ConfusionMatrix
                  labels={result.confusion_matrix.labels}
                  matrix={result.confusion_matrix.matrix}
                />
              </Grid>
            )}
            {result.feature_importances && result.feature_importances.length > 0 && (
              <Grid item xs={12} md={6}>
                <FeatureImportanceChart data={result.feature_importances} />
              </Grid>
            )}
          </Grid>
        </Stack>
      </CardContent>
    </Card>
  );
}
