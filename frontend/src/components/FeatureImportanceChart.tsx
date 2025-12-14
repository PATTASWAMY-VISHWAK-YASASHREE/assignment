import { Card, CardContent, CardHeader } from "@mui/material";
import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
  Legend,
} from "chart.js";

import { FeatureImportance } from "../types";

ChartJS.register(CategoryScale, LinearScale, BarElement, Tooltip, Legend);

export default function FeatureImportanceChart({ data }: { data: FeatureImportance[] }) {
  if (!data.length) return null;

  const labels = data.map((d) => d.name);
  const values = data.map((d) => d.importance);

  return (
    <Card>
      <CardHeader title="Feature Importance" />
      <CardContent>
        <Bar
          data={{
            labels,
            datasets: [
              {
                label: "Importance",
                data: values,
                backgroundColor: "rgba(79, 70, 229, 0.6)",
              },
            ],
          }}
          options={{
            responsive: true,
            plugins: {
              legend: { display: false },
            },
            scales: {
              x: { ticks: { autoSkip: false, maxRotation: 45, minRotation: 45 } },
            },
          }}
        />
      </CardContent>
    </Card>
  );
}
