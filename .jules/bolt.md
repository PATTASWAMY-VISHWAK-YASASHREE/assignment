## 2024-05-23 - Missing Config Blocking Test
**Learning:** The `dataset_service.py` relied on `settings.MAX_UPLOAD_SIZE_BYTES` which was missing from `backend/app/core/config.py`. This prevented even basic file uploads from working, blocking reproduction of other issues.
**Action:** Always verify basic configuration consistency when encountering seemingly unrelated errors (like "Settings object has no attribute").

## 2024-05-23 - Massive Memory Overhead From Redundant Pandas Copies
**Learning:** `dataset_service.get_dataset` returns a reference to the shared DataFrame from an in-memory dictionary. Calling `.copy()` on this immediately duplicates the entire memory footprint. For a large dataset (e.g. 1M rows x 100 columns taking ~840MB), doing `df = dataset_service.get_dataset(...).copy()` and then `df_features = df[feature_cols].copy()` pushes memory from ~840MB to ~2.4GB just in data prep.
**Action:** When working with shared datasets in memory, only copy the specific subsets or slices (e.g., `df_features = df[feature_cols].copy()`) you intend to mutate, rather than preemptively copying the entire dataset first.
