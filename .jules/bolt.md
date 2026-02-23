## 2024-05-23 - Missing Config Blocking Test
**Learning:** The `dataset_service.py` relied on `settings.MAX_UPLOAD_SIZE_BYTES` which was missing from `backend/app/core/config.py`. This prevented even basic file uploads from working, blocking reproduction of other issues.
**Action:** Always verify basic configuration consistency when encountering seemingly unrelated errors (like "Settings object has no attribute").

## 2024-05-24 - Imputing Values Optimization
**Learning:** Calculating `median()` and `mode()` for all columns and using `fillna` with a dictionary was consistently slower (0.6x speedup) than iterating over columns and calling `fillna` individually for this dataset structure.
**Action:** Always benchmark pandas optimizations; theoretical wins (vectorization/bulk operations) can be offset by overhead of intermediate structures like DataFrames returned by `mode()`.
