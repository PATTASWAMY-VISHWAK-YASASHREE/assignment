## 2024-05-23 - Missing Config Blocking Test
**Learning:** The `dataset_service.py` relied on `settings.MAX_UPLOAD_SIZE_BYTES` which was missing from `backend/app/core/config.py`. This prevented even basic file uploads from working, blocking reproduction of other issues.
**Action:** Always verify basic configuration consistency when encountering seemingly unrelated errors (like "Settings object has no attribute").

## 2024-05-24 - Streaming Uploads
**Learning:** `UploadFile` in FastAPI/Starlette wraps a `SpooledTemporaryFile`. Reading it into a `bytearray` for size checking duplicates the file in memory.
**Action:** Use `file.file.seek(0, 2)` and `tell()` to check size, then stream `file.file` directly to consumers (like Pandas) to halve peak memory usage.
