import { useEffect, useMemo } from "react";
import ReactFlow, { Background, Controls, Edge, Node, useNodesState } from "reactflow";
import "reactflow/dist/style.css";

import { usePipelineStore } from "../store/usePipelineStore";

const statusColor = (active: boolean) => (active ? "#10b981" : "#94a3b8");

export default function FlowCanvas() {
  const dataset = usePipelineStore((s) => s.dataset);
  const preprocess = usePipelineStore((s) => s.preprocessSteps);
  const split = usePipelineStore((s) => s.split);
  const model = usePipelineStore((s) => s.model);
  const result = usePipelineStore((s) => s.result);

  const initialNodes: Node[] = useMemo(
    () => [
      { id: "data", position: { x: 0, y: 50 }, data: { label: "Data" }, style: { borderWidth: 2 } },
      { id: "prep", position: { x: 200, y: 50 }, data: { label: "Preprocess" }, style: { borderWidth: 2 } },
      { id: "split", position: { x: 400, y: 50 }, data: { label: "Split" }, style: { borderWidth: 2 } },
      { id: "model", position: { x: 600, y: 50 }, data: { label: "Model" }, style: { borderWidth: 2 } },
      { id: "result", position: { x: 800, y: 50 }, data: { label: "Result" }, style: { borderWidth: 2 } },
    ],
    []
  );

  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);

  const edges: Edge[] = [
    { id: "e1", source: "data", target: "prep", animated: true },
    { id: "e2", source: "prep", target: "split", animated: true },
    { id: "e3", source: "split", target: "model", animated: true },
    { id: "e4", source: "model", target: "result", animated: true },
  ];

  useEffect(() => {
    setNodes((nds) =>
      nds.map((n) => {
        if (n.id === "data") {
          return { ...n, data: { label: `Data\n${dataset ? "ready" : "pending"}` }, style: { ...n.style, borderColor: statusColor(!!dataset) } };
        }
        if (n.id === "prep") {
          return { ...n, data: { label: `Preprocess\n${preprocess.length} step(s)` }, style: { ...n.style, borderColor: statusColor(preprocess.length > 0) } };
        }
        if (n.id === "split") {
          return { ...n, data: { label: `Split\nTest ${Math.round(split.test_size * 100)}%` }, style: { ...n.style, borderColor: statusColor(true) } };
        }
        if (n.id === "model") {
          return { ...n, data: { label: `Model\n${model || "select"}` }, style: { ...n.style, borderColor: statusColor(!!model) } };
        }
        if (n.id === "result") {
          return { ...n, data: { label: `Result\n${result ? "done" : "waiting"}` }, style: { ...n.style, borderColor: statusColor(!!result) } };
        }
        return n;
      })
    );
  }, [dataset, model, preprocess.length, result, split.test_size, setNodes]);

  return (
    <div className="flow-container" style={{ minHeight: 180 }}>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        fitView
        nodesConnectable={false}
        elementsSelectable={false}
      >
        <Background />
        <Controls showFitView={false} showInteractive={false} />
      </ReactFlow>
    </div>
  );
}
