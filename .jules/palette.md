## 2024-05-22 - Immediate Validation for Code Inputs
**Learning:** Users often paste JSON or code snippets and don't realize they have syntax errors until they hit submit. Immediate validation (e.g., on blur) significantly reduces frustration and round-trip time.
**Action:** When designing inputs for structured data (JSON, YAML, etc.), always implement client-side validation that triggers on blur or pause, providing specific syntax error feedback before submission.
