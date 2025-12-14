import { Container, Grid, Stack, Typography, Box } from "@mui/material";

import UploadCard from "./components/UploadCard";
import DataOverview from "./components/DataOverview";
import PreprocessCard from "./components/PreprocessCard";
import SplitCard from "./components/SplitCard";
import ModelCard from "./components/ModelCard";
import RunPanel from "./components/RunPanel";
import ResultsPanel from "./components/ResultsPanel";
import FlowCanvas from "./components/FlowCanvas";

export default function App() {
  return (
    <Container maxWidth="xl" sx={{ py: 4 }}>
      <Stack spacing={3}>
        <Box display="flex" alignItems="center" justifyContent="space-between" flexWrap="wrap" gap={2}>
          <Box>
            <Typography variant="h4" fontWeight={700}>
              No-Code ML Pipeline Builder
            </Typography>
            <Typography color="text.secondary">
              Drag-and-drop inspired flow to build ML pipelines without code.
            </Typography>
          </Box>
        </Box>

        <FlowCanvas />

        <Grid container spacing={2}>
          <Grid item xs={12} md={6} lg={4}>
            <UploadCard />
          </Grid>
          <Grid item xs={12} md={6} lg={8}>
            <DataOverview />
          </Grid>
          <Grid item xs={12} md={6} lg={6}>
            <PreprocessCard />
          </Grid>
          <Grid item xs={12} md={6} lg={6}>
            <SplitCard />
          </Grid>
          <Grid item xs={12} md={6} lg={6}>
            <ModelCard />
          </Grid>
          <Grid item xs={12} md={6} lg={6}>
            <RunPanel />
          </Grid>
          <Grid item xs={12}>
            <ResultsPanel />
          </Grid>
        </Grid>
      </Stack>
    </Container>
  );
}
