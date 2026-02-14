## 2024-05-23 - Missing Config Blocking Test
**Learning:** The `dataset_service.py` relied on `settings.MAX_UPLOAD_SIZE_BYTES` which was missing from `backend/app/core/config.py`. This prevented even basic file uploads from working, blocking reproduction of other issues.
**Action:** Always verify basic configuration consistency when encountering seemingly unrelated errors (like "Settings object has no attribute").

## 2025-02-28 - Efficient Upload Size Checking
**Learning:** `FastAPI`'s `UploadFile` exposes a file-like object via `.file` which is seekable (even if it's a `SpooledTemporaryFile`). Checking upload size via `seek(0, 2)` + `tell()` is vastly more efficient than reading chunks into memory, especially for large files where we want to reject them early or process them without duplicating memory.
**Action:** Prefer `file.seek(0, 2)` for size checks on `UploadFile` and pass the file object directly to consumers (like `pandas.read_csv`) instead of buffering content into `bytes`.
