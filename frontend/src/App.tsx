import { Container, Grid, Stack, Typography, Box, Divider } from "@mui/material";

import UploadCard from "./components/UploadCard";
import DataOverview from "./components/DataOverview";
import PreprocessCard from "./components/PreprocessCard";
import SplitCard from "./components/SplitCard";
import ModelCard from "./components/ModelCard";
import RunPanel from "./components/RunPanel";
import ResultsPanel from "./components/ResultsPanel";
import FlowCanvas from "./components/FlowCanvas";
import PlaygroundCard from "./components/PlaygroundCard";

export default function App() {
  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Stack spacing={3}>
        <Box display="flex" alignItems="center" justifyContent="space-between" flexWrap="wrap" gap={2}>
          <Box>
            <Typography variant="h4" fontWeight={700}>
              No-Code ML Pipeline Builder
            </Typography>
            <Typography color="text.secondary">
              Guided steps to upload data, configure preprocessing, and run models.
            </Typography>
          </Box>
        </Box>

        <FlowCanvas />

        <Grid container rowSpacing={3} columnSpacing={3} alignItems="stretch">
          <Grid item xs={12} md={6}>
            <UploadCard />
          </Grid>
          <Grid item xs={12} md={6}>
            <DataOverview />
          </Grid>

          <Grid item xs={12} md={6}>
            <PreprocessCard />
          </Grid>
          <Grid item xs={12} md={6}>
            <SplitCard />
          </Grid>

          <Grid item xs={12} md={6}>
            <ModelCard />
          </Grid>
          <Grid item xs={12} md={6}>
            <RunPanel />
          </Grid>
          <Grid item xs={12}>
            <ResultsPanel />
          </Grid>
        </Grid>

        <Divider textAlign="left">Playground</Divider>
        <Box>
          <PlaygroundCard />
        </Box>
      </Stack>
    </Container>
  );
}
