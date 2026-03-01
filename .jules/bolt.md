## 2024-05-23 - Missing Config Blocking Test
**Learning:** The `dataset_service.py` relied on `settings.MAX_UPLOAD_SIZE_BYTES` which was missing from `backend/app/core/config.py`. This prevented even basic file uploads from working, blocking reproduction of other issues.
**Action:** Always verify basic configuration consistency when encountering seemingly unrelated errors (like "Settings object has no attribute").

## 2026-03-01 - Optimization of np.unique on object arrays
**Learning:** `np.unique` is significantly slower when applied to object arrays or pandas Series containing objects (such as strings). In the case of determining stratification variables during `train_test_split`, switching from `len(np.unique(target)) > 1` to `pd.Series(target).nunique() > 1` provided an ~18x speedup on arrays of string labels.
**Action:** When counting unique values on categorical or object-type pandas variables, always prefer the pandas-native `.nunique()` over numpy's `np.unique()`.
