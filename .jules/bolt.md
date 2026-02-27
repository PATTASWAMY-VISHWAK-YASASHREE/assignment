## 2024-05-23 - Missing Config Blocking Test
**Learning:** The `dataset_service.py` relied on `settings.MAX_UPLOAD_SIZE_BYTES` which was missing from `backend/app/core/config.py`. This prevented even basic file uploads from working, blocking reproduction of other issues.
**Action:** Always verify basic configuration consistency when encountering seemingly unrelated errors (like "Settings object has no attribute").

## 2024-05-24 - Pandas Series Creation Overhead
**Learning:** Creating a `pd.Series` from a numpy array just to use `.isin()` introduces significant overhead (~10x slower) compared to using `np.isin()` directly on the array, especially inside tight loops or large datasets.
**Action:** Prefer `np.isin()` for filtering numpy arrays or lists when advanced Pandas indexing features are not required.
