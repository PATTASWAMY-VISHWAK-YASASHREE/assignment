## 2024-05-23 - Missing Config Blocking Test
**Learning:** The `dataset_service.py` relied on `settings.MAX_UPLOAD_SIZE_BYTES` which was missing from `backend/app/core/config.py`. This prevented even basic file uploads from working, blocking reproduction of other issues.
**Action:** Always verify basic configuration consistency when encountering seemingly unrelated errors (like "Settings object has no attribute").

## 2024-05-23 - Pandas value_counts vs numpy unique for Categorical Arrays
**Learning:** Using `np.unique` to count frequencies or find unique elements in a categorical (string/object) array is extremely slow compared to using Pandas' built-in `pd.Series(target).value_counts()` and `pd.Series(target).nunique()`. The Pandas functions achieved up to a ~20x speedup for finding and filtering rare classes on string targets.
**Action:** When working with DataFrames/Series, especially involving categorical or object data types, prefer Pandas' native functions like `value_counts()` and `nunique()` over converting to/from `numpy` functions like `np.unique`. Always reset the index when subsetting with `loc` or boolean masks to prevent misalignment with other DataFrames.
