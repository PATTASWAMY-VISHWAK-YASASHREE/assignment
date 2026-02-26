## 2024-05-23 - Missing Config Blocking Test
**Learning:** The `dataset_service.py` relied on `settings.MAX_UPLOAD_SIZE_BYTES` which was missing from `backend/app/core/config.py`. This prevented even basic file uploads from working, blocking reproduction of other issues.
**Action:** Always verify basic configuration consistency when encountering seemingly unrelated errors (like "Settings object has no attribute").

## 2024-05-24 - Pandas Optimization and Index Safety
**Learning:** `pd.Series.value_counts` is ~17x faster than `np.unique` for categorical data. However, converting numpy arrays to Series for this optimization introduced a critical index misalignment bug because the Series retained original indices while the feature DataFrame was reset.
**Action:** When optimizing with Pandas, explicitly check index alignment and use `reset_index(drop=True)` on all aligned data structures after filtering.
