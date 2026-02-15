## 2024-05-23 - Missing Config Blocking Test
**Learning:** The `dataset_service.py` relied on `settings.MAX_UPLOAD_SIZE_BYTES` which was missing from `backend/app/core/config.py`. This prevented even basic file uploads from working, blocking reproduction of other issues.
**Action:** Always verify basic configuration consistency when encountering seemingly unrelated errors (like "Settings object has no attribute").

## 2025-02-18 - [Streaming Upload Optimization]
**Learning:** Reading large `UploadFile` content into a `bytearray` manually (chunk by chunk) is significantly slower (2x-3x) and memory-intensive compared to passing `file.file` (SpooledTemporaryFile) directly to Pandas. `UploadFile.seek(0, 2)` can be used to check size without reading content.
**Action:** Always prefer passing file-like objects directly to libraries (Pandas, PIL, etc.) instead of buffering in memory.
