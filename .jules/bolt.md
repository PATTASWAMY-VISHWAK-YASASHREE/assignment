## 2024-05-23 - Missing Config Blocking Test
**Learning:** The `dataset_service.py` relied on `settings.MAX_UPLOAD_SIZE_BYTES` which was missing from `backend/app/core/config.py`. This prevented even basic file uploads from working, blocking reproduction of other issues.
**Action:** Always verify basic configuration consistency when encountering seemingly unrelated errors (like "Settings object has no attribute").

## 2024-05-24 - Pandas value_counts vs np.unique
**Learning:** `pd.Series.value_counts(sort=False)` is ~5x faster than `np.unique(return_counts=True)` for frequency counting, even when input is a numpy array. `np.unique` always sorts the output, which is O(N log N), while `value_counts` (hash-based) is O(N).
**Action:** Prefer `value_counts(sort=False)` for frequency counting and `nunique()` for counting unique values over `np.unique` unless sorted output is strictly required.
