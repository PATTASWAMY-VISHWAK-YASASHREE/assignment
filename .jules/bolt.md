## 2024-05-23 - Missing Config Blocking Test
**Learning:** The `dataset_service.py` relied on `settings.MAX_UPLOAD_SIZE_BYTES` which was missing from `backend/app/core/config.py`. This prevented even basic file uploads from working, blocking reproduction of other issues.
**Action:** Always verify basic configuration consistency when encountering seemingly unrelated errors (like "Settings object has no attribute").

## 2024-10-24 - Convert Predictions via array.tolist()
**Learning:** In Python backend data science code, converting scikit-learn NumPy array predictions to standard Python lists using a list comprehension with per-element `isinstance` checks creates significant overhead.
**Action:** Use the native `array.tolist()` method to provide a substantial speedup for the prediction step by bypassing this loop overhead entirely.
