## 2024-05-23 - Missing Config Blocking Test
**Learning:** The `dataset_service.py` relied on `settings.MAX_UPLOAD_SIZE_BYTES` which was missing from `backend/app/core/config.py`. This prevented even basic file uploads from working, blocking reproduction of other issues.
**Action:** Always verify basic configuration consistency when encountering seemingly unrelated errors (like "Settings object has no attribute").

## 2024-05-23 - NumPy np.unique Performance Bottleneck on Object Arrays
**Learning:** `np.unique` behaves as an $O(N \log N)$ operation because it sorts the array to find unique values and counts. For categorical target columns containing strings (object arrays in numpy), this sorting overhead is massive. In testing, counting 10 million string values took ~30.5 seconds with `np.unique` vs ~0.5 seconds with `pd.Series.nunique(dropna=False)`.
**Action:** Replace `np.unique` with pandas hash-based equivalents (`value_counts(sort=False, dropna=False)` or `nunique(dropna=False)`) when checking for uniqueness or counting occurrences in categorical variables, especially within large datasets.
