## 2024-05-23 - [Pandas Loop vs Vectorization]
**Learning:** Surprisingly, iterating over columns and calling `fillna()` individually was FASTER than `df[subset].fillna()` or `df.fillna(dict)` for datasets with ~200 columns.
**Action:** Always benchmark "obvious" vectorization optimizations in pandas, as overhead of subset creation and large-scale operations can outweigh Python loop overhead for medium-width data.

## 2024-05-23 - [FastAPI UploadFile Optimization]
**Learning:** `UploadFile` methods are async wrappers around synchronous file objects (`SpooledTemporaryFile`). `await file.read()` buffers data. For heavy I/O like pandas parsing, access `file.file` directly to pass the file handle to C-extensions, avoiding double memory usage.
**Action:** Use `file.file` for integration with libraries that accept file-like objects (pandas, Pillow, etc.) to stream data.
