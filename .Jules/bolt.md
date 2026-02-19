
## 2025-02-17 - File Upload Streaming
**Learning:** `UploadFile` in FastAPI/Starlette exposes the underlying file object via `.file`, which can be passed directly to pandas `read_csv` or `read_excel`. This avoids reading the entire file into memory (bytes) first, significantly reducing peak memory usage (observed ~55% reduction).
**Action:** Always prefer passing file-like objects to pandas read functions instead of buffering content into bytes, especially for potentially large uploads.

## 2025-02-17 - Pandas Fillna Optimization
**Learning:** Creating a dictionary of fill values and calling `df.fillna(dict)` was measured to be slower (0.69x) than iterating over columns and filling them individually for a 100k row dataset. This counter-intuitive result suggests that the overhead of dictionary construction or internal pandas handling might outweigh the benefits of a single call for this specific operation/version.
**Action:** Benchmark "optimizations" before applying them. Vectorization isn't always faster if it involves complex setup or if the underlying library handles loops efficiently.
