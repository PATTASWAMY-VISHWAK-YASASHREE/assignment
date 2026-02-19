## 2024-05-23 - Missing Config Blocking Test
**Learning:** The `dataset_service.py` relied on `settings.MAX_UPLOAD_SIZE_BYTES` which was missing from `backend/app/core/config.py`. This prevented even basic file uploads from working, blocking reproduction of other issues.
**Action:** Always verify basic configuration consistency when encountering seemingly unrelated errors (like "Settings object has no attribute").

## 2024-05-24 - Efficient File Size Check in FastAPI
**Learning:** FastAPI/Starlette `UploadFile` (specifically `SpooledTemporaryFile`) supports `seek(0, 2)` and `tell()` to check file size without reading the content into memory. This avoids loading large files into RAM just to check size, which is critical for memory efficiency.
**Action:** Use `file.file.seek(0, 2)` and `tell()` instead of `await file.read()` for size validation.
