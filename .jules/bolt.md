## 2024-05-23 - Missing Config Blocking Test
**Learning:** The `dataset_service.py` relied on `settings.MAX_UPLOAD_SIZE_BYTES` which was missing from `backend/app/core/config.py`. This prevented even basic file uploads from working, blocking reproduction of other issues.
**Action:** Always verify basic configuration consistency when encountering seemingly unrelated errors (like "Settings object has no attribute").

## 2024-05-23 - Pandas value_counts speedup over np.unique for categorical data
**Learning:** `np.unique(..., return_counts=True)` and `len(np.unique(...))` are significant bottlenecks for categorical (object/string) data, taking ~6.4 seconds for 10M rows vs ~0.4s for `pd.Series(target).nunique()` and ~0.2s for `pd.Series(target).value_counts(sort=False, dropna=False)`. It provides a ~17x speedup for counting operations. Crucially, when applying boolean masks to drop rows based on value counts, the index of the resulting filtered `pd.Series` must be explicitly reset to ensure alignment with other index-reset Pandas DataFrames.
**Action:** Always prefer `pd.Series.value_counts(sort=False, dropna=False)` and `pd.Series.nunique()` over `np.unique` when calculating frequencies or unique values on categorical arrays or pandas Series. Remember to explicitly reset the index of filtered pandas objects to maintain alignment in subsequent operations.
