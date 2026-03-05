## 2024-05-23 - Missing Config Blocking Test
**Learning:** The `dataset_service.py` relied on `settings.MAX_UPLOAD_SIZE_BYTES` which was missing from `backend/app/core/config.py`. This prevented even basic file uploads from working, blocking reproduction of other issues.
**Action:** Always verify basic configuration consistency when encountering seemingly unrelated errors (like "Settings object has no attribute").
## 2026-03-05 - Fast Unique Count For Categorical Targets
**Learning:** In Pandas, computing uniqueness for categorical arrays using `pd.Series(target).nunique(dropna=False)` is significantly faster (~18x-30x) than using `len(np.unique(target))`. `np.unique` struggles with object arrays, sorting, and type checking, while `nunique` uses highly optimized hash tables.
**Action:** Always prefer `nunique` or `value_counts` on Pandas Series over `np.unique` when determining uniqueness or counting frequencies, especially for non-numeric or string arrays in the codebase.
