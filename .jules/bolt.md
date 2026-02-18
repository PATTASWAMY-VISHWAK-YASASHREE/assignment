## 2024-05-23 - Missing Config Blocking Test
**Learning:** The `dataset_service.py` relied on `settings.MAX_UPLOAD_SIZE_BYTES` which was missing from `backend/app/core/config.py`. This prevented even basic file uploads from working, blocking reproduction of other issues.
**Action:** Always verify basic configuration consistency when encountering seemingly unrelated errors (like "Settings object has no attribute").

## 2024-05-24 - Efficient File Upload Handling
**Learning:** `Starlette.UploadFile` wrappers provide a `file` attribute which is a file-like object (`SpooledTemporaryFile`) supporting `seek` and `tell`. Reading the entire file into a `bytearray` (as was done in `dataset_service.py`) duplicates memory usage and is inefficient for large files. `pandas.read_csv` and `read_excel` accept file-like objects directly, allowing zero-copy streaming from the upload buffer.
**Action:** Use `file.file` directly for size checks and pass it to downstream libraries (like Pandas) instead of buffering into memory, especially for large uploads.
