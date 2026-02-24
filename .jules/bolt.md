## 2024-05-23 - Missing Config Blocking Test
**Learning:** The `dataset_service.py` relied on `settings.MAX_UPLOAD_SIZE_BYTES` which was missing from `backend/app/core/config.py`. This prevented even basic file uploads from working, blocking reproduction of other issues.
**Action:** Always verify basic configuration consistency when encountering seemingly unrelated errors (like "Settings object has no attribute").
## 2024-05-24 - Zero-Copy File Uploads
**Learning:** The dataset upload service was reading the entire file into a `bytearray` (RAM) just to check the size, then wrapping it in `BytesIO` (more RAM) for Pandas. This meant a 100MB upload consumed ~200MB+ RAM and added GC pressure.
**Action:** Use `file.file.seek(0, 2)` to check size and pass `file.file` directly to `pd.read_csv`, enabling streaming uploads with constant memory usage.
