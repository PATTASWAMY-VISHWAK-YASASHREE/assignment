## 2024-05-24 - Dataset Upload Memory Optimization
**Learning:** Initial implementation of `save_dataset` read the entire file into a `bytearray` to check size, effectively doubling memory usage. Starlette's `UploadFile.file` is a `SpooledTemporaryFile` that can be passed directly to Pandas.
**Action:** When handling large file uploads, always prefer seeking the file object for size checks and streaming directly to consumers (like Pandas or S3) to avoid O(N) memory overhead.
