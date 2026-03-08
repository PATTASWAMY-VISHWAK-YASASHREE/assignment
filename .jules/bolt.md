## 2024-05-23 - Missing Config Blocking Test
**Learning:** The `dataset_service.py` relied on `settings.MAX_UPLOAD_SIZE_BYTES` which was missing from `backend/app/core/config.py`. This prevented even basic file uploads from working, blocking reproduction of other issues.
**Action:** Always verify basic configuration consistency when encountering seemingly unrelated errors (like "Settings object has no attribute").

## 2024-05-23 - Predict Conversion Optimization
**Learning:** Using list comprehensions with `isinstance` checks inside a loop to convert scikit-learn numpy array predictions back to standard python types is a large overhead. Natively casting numpy arrays to lists via `.tolist()` provides a ~15x speedup for the prediction step by bypassing per-element type checking loop overhead.
**Action:** Prefer `array.tolist()` when natively converting numpy arrays of predictions directly into lists, especially in code handling bulk data processing.
