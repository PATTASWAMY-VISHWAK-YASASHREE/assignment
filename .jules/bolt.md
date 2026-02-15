## 2024-05-23 - Missing Config Blocking Test
**Learning:** The `dataset_service.py` relied on `settings.MAX_UPLOAD_SIZE_BYTES` which was missing from `backend/app/core/config.py`. This prevented even basic file uploads from working, blocking reproduction of other issues.
**Action:** Always verify basic configuration consistency when encountering seemingly unrelated errors (like "Settings object has no attribute").

## 2024-05-24 - Efficient File Uploads in FastAPI
**Learning:** `UploadFile` in FastAPI/Starlette (v0.41.3) does not support `seek(offset, whence)` in its async `seek` method; it only accepts `offset`. To check file size by seeking to the end, one must access the underlying synchronous file object (`file.file`) directly. Also, reading `UploadFile` into a `bytearray` for size checking duplicates the entire file in memory, causing O(N) memory overhead.
**Action:** For large file uploads, always use `file.file.seek(0, 2)` and `file.file.tell()` to check size, and pass the file object directly to processing functions (e.g., Pandas) to enable zero-copy streaming.
