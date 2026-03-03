## 2024-05-23 - Missing Config Blocking Test
**Learning:** The `dataset_service.py` relied on `settings.MAX_UPLOAD_SIZE_BYTES` which was missing from `backend/app/core/config.py`. This prevented even basic file uploads from working, blocking reproduction of other issues.
**Action:** Always verify basic configuration consistency when encountering seemingly unrelated errors (like "Settings object has no attribute").

## 2024-05-23 - pandas.nunique() vs numpy.unique()
**Learning:** In Pandas, calculating the number of unique values for object arrays (like string labels or categories) using `pd.Series(target).nunique()` provides a significant performance gain (~18x-30x speedup depending on length and structure) compared to using `len(np.unique(target))`. `np.unique` behaves poorly on large arrays of strings.
**Action:** Use `pd.Series.nunique()` when you only need the count of unique classes from categorical data arrays or Pandas Series, instead of calculating and counting all unique items with numpy.
