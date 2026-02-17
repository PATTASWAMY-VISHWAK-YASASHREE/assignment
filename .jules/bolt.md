## 2024-05-23 - Missing Config Blocking Test
**Learning:** The `dataset_service.py` relied on `settings.MAX_UPLOAD_SIZE_BYTES` which was missing from `backend/app/core/config.py`. This prevented even basic file uploads from working, blocking reproduction of other issues.
**Action:** Always verify basic configuration consistency when encountering seemingly unrelated errors (like "Settings object has no attribute").

## 2026-02-17 - Dataset Upload Memory Optimization
**Learning:** `dataset_service.save_dataset` was inefficiently reading the entire uploaded file into a `bytearray` loop before parsing. This doubled memory consumption and increased latency for large files.
**Action:** Utilize `file.file.seek(0, 2)` for size validation and pass the underlying `file.file` object directly to Pandas (via `run_in_executor`) to enable streaming parsing without intermediate memory buffering.
