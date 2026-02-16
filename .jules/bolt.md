## 2024-05-23 - Streaming File Uploads to Pandas
**Learning:** Reading large files (100MB) into a `bytearray` before processing in Pandas doubles memory usage and adds latency. `UploadFile.file` (SpooledTemporaryFile) can be passed directly to `pd.read_csv`/`pd.read_excel` for zero-copy streaming.
**Action:** Use `file.file` directly for file processing tasks, ensuring to check size via `seek(0, 2); tell()` instead of reading content.

## 2024-05-23 - Pandas Vectorization Overhead
**Learning:** Attempting to vectorize median/mode imputation on a DataFrame was slower (0.32s) than the iterative column-wise approach (0.16s) for a 50k row dataset. The overhead of creating new DataFrames/Series in bulk operations outweighed the loop cost for simple aggregations.
**Action:** Measure before optimizing "obvious" loops in Pandas.
