## 2024-05-23 - Missing Config Blocking Test
**Learning:** The `dataset_service.py` relied on `settings.MAX_UPLOAD_SIZE_BYTES` which was missing from `backend/app/core/config.py`. This prevented even basic file uploads from working, blocking reproduction of other issues.
**Action:** Always verify basic configuration consistency when encountering seemingly unrelated errors (like "Settings object has no attribute").

## 2024-05-25 - Pandas unique count optimization
**Learning:** For categorical (object/string) data in pandas/numpy arrays, `pd.Series.value_counts(sort=False, dropna=False)` is significantly faster (~17x speedup on large arrays) than using `np.unique(return_counts=True)` because pandas leverages hash maps under the hood instead of sorting `O(n log n)` the data.
**Action:** Use `value_counts` instead of `np.unique` when computing frequencies on categorical features and targets.
