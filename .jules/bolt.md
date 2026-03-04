## 2024-05-23 - Missing Config Blocking Test
**Learning:** The `dataset_service.py` relied on `settings.MAX_UPLOAD_SIZE_BYTES` which was missing from `backend/app/core/config.py`. This prevented even basic file uploads from working, blocking reproduction of other issues.
**Action:** Always verify basic configuration consistency when encountering seemingly unrelated errors (like "Settings object has no attribute").

## 2024-05-23 - Pandas value_counts and nunique vs np.unique
**Learning:** Calculating unique values and their frequencies for categorical (object/string) arrays using Pandas `value_counts(sort=False, dropna=False)` and `nunique(dropna=False)` is significantly faster (~17-30x) than using NumPy's `np.unique` because `np.unique` must sort the array first (O(N log N)) while Pandas uses an O(N) hash table approach. Using `dropna=False` is critical when replacing `np.unique` to maintain exact behavior.
**Action:** Always prefer `pd.Series.value_counts(sort=False)` and `pd.Series.nunique()` over `np.unique` for frequency counts and unique item counts in Pandas/categorical contexts.
