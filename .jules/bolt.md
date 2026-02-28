## 2024-05-23 - Missing Config Blocking Test
**Learning:** The `dataset_service.py` relied on `settings.MAX_UPLOAD_SIZE_BYTES` which was missing from `backend/app/core/config.py`. This prevented even basic file uploads from working, blocking reproduction of other issues.
**Action:** Always verify basic configuration consistency when encountering seemingly unrelated errors (like "Settings object has no attribute").

## 2025-02-28 - Bulk Fillna Performance in Pandas 3
**Learning:** In Pandas 3.0.1, applying `fillna` with a dictionary mapping for bulk imputation (`df.fillna(value=fill_dict)`) is significantly slower than iterating through columns and calling `fillna` on each `pd.Series` individually. However, computing the fill values (like medians) in bulk (`df[numeric_cols].median().to_dict()`) outside the loop is still faster than computing them per-column inside the loop.
**Action:** Always compute statistical metrics (medians) in bulk for a subset of columns using vectorized dataframe operations, but apply the resulting fill values using a fast `for` loop over the columns.
