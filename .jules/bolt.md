## 2024-05-23 - Missing Config Blocking Test
**Learning:** The `dataset_service.py` relied on `settings.MAX_UPLOAD_SIZE_BYTES` which was missing from `backend/app/core/config.py`. This prevented even basic file uploads from working, blocking reproduction of other issues.
**Action:** Always verify basic configuration consistency when encountering seemingly unrelated errors (like "Settings object has no attribute").

## 2025-03-03 - Numpy Unique vs Pandas Unique Methods for Categorical
**Learning:** For counting unique values or getting frequencies in categorical arrays (object/string data types), `pd.Series(array).nunique(dropna=False)` and `pd.Series(array).value_counts(sort=False, dropna=False)` offer a significant (~17x - 30x) performance improvement over using `np.unique` directly. However, using `.value_counts()` does not guarantee deterministic order like `np.unique` might, and so if error messages format the categories, an explicit `sorted(dict.keys())` may be required to maintain test pass logic.
**Action:** When handling categorical features or labels, default to Pandas' unique counting methods instead of NumPy's.
