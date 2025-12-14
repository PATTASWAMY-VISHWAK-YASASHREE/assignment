import { Card, CardContent, CardHeader, Table, TableBody, TableCell, TableHead, TableRow, Typography } from "@mui/material";

import { ConfusionMatrix as CMType } from "../types";

export function ConfusionMatrix({ matrix, labels }: CMType) {
  return (
    <Card>
      <CardHeader title="Confusion Matrix" />
      <CardContent>
        <Typography variant="body2" color="text.secondary" mb={1}>
          Rows: Actual • Columns: Predicted
        </Typography>
        <Table size="small">
          <TableHead>
            <TableRow>
              <TableCell>Actual / Pred</TableCell>
              {labels.map((l) => (
                <TableCell key={`h-${l}`} align="center">
                  {l}
                </TableCell>
              ))}
            </TableRow>
          </TableHead>
          <TableBody>
            {matrix.map((row, i) => (
              <TableRow key={`r-${labels[i]}`}>
                <TableCell>{labels[i]}</TableCell>
                {row.map((value, j) => (
                  <TableCell key={`c-${i}-${j}`} align="center">
                    {value}
                  </TableCell>
                ))}
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </CardContent>
    </Card>
  );
}
