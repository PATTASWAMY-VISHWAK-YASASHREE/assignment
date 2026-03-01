## 2024-05-23 - Missing Config Blocking Test
**Learning:** The `dataset_service.py` relied on `settings.MAX_UPLOAD_SIZE_BYTES` which was missing from `backend/app/core/config.py`. This prevented even basic file uploads from working, blocking reproduction of other issues.
**Action:** Always verify basic configuration consistency when encountering seemingly unrelated errors (like "Settings object has no attribute").

## 2024-05-24 - Bulk calculation vs bulk assignment in Pandas 3.0.1
**Learning:** Calculating medians in bulk for numeric columns (`df[numeric_cols].median().to_dict()`) before iterating for imputation provides a significant performance gain over calculating them column-by-column inside a loop. However, applying `fillna` with a dictionary (`df.fillna(value=dict)`) for bulk imputation is slower than iterating through columns and calling `fillna` on each `pd.Series` individually in Pandas 3.0.1.
**Action:** Always measure and combine bulk calculation with per-column assignment in Pandas loops when optimizing imputation or similar dataframe operations.
