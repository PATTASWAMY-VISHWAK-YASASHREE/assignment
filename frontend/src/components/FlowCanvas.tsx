import { useMemo } from "react";
import ReactFlow, { Background, Controls, Edge, Node } from "reactflow";
import "reactflow/dist/style.css";

import { usePipelineStore } from "../store/usePipelineStore";

const statusColor = (active: boolean) => (active ? "#10b981" : "#94a3b8");

export default function FlowCanvas() {
  const dataset = usePipelineStore((s) => s.dataset);
  const target = usePipelineStore((s) => s.targetColumn);
  const preprocess = usePipelineStore((s) => s.preprocessSteps);
  const split = usePipelineStore((s) => s.split);
  const model = usePipelineStore((s) => s.model);
  const result = usePipelineStore((s) => s.result);

  const nodes: Node[] = useMemo(
    () => [
      {
        id: "data",
        position: { x: 0, y: 50 },
        data: { label: `Data\n${dataset ? "ready" : "pending"}` },
        style: { borderColor: statusColor(!!dataset), borderWidth: 2 },
      },
      {
        id: "prep",
        position: { x: 200, y: 50 },
        data: { label: `Preprocess\n${preprocess.length} step(s)` },
        style: { borderColor: statusColor(preprocess.length > 0), borderWidth: 2 },
      },
      {
        id: "split",
        position: { x: 400, y: 50 },
        data: { label: `Split\nTest ${Math.round(split.test_size * 100)}%` },
        style: { borderColor: statusColor(true), borderWidth: 2 },
      },
      {
        id: "model",
        position: { x: 600, y: 50 },
        data: { label: `Model\n${model || "select"}` },
        style: { borderColor: statusColor(!!model), borderWidth: 2 },
      },
      {
        id: "result",
        position: { x: 800, y: 50 },
        data: { label: `Result\n${result ? "done" : "waiting"}` },
        style: { borderColor: statusColor(!!result), borderWidth: 2 },
      },
    ],
    [dataset, model, preprocess.length, result, split.test_size]
  );

  const edges: Edge[] = [
    { id: "e1", source: "data", target: "prep", animated: true },
    { id: "e2", source: "prep", target: "split", animated: true },
    { id: "e3", source: "split", target: "model", animated: true },
    { id: "e4", source: "model", target: "result", animated: true },
  ];

  return (
    <div className="flow-container">
      <ReactFlow nodes={nodes} edges={edges} fitView nodesConnectable={false} elementsSelectable={false}>
        <Background />
        <Controls showFitView={false} showInteractive={false} />
      </ReactFlow>
    </div>
  );
}
