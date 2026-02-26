## 2024-05-23 - JSON Input Validation & Accessibility

**Learning:** Users entering raw JSON often make syntax errors. Providing immediate feedback via `onBlur` and using a `monospace` font significantly improves the experience. Additionally, wrapping dynamic results in `aria-live="polite"` is critical for screen reader users to know when async operations complete.
**Action:** Always pair raw code/JSON inputs with immediate validation and monospace styling. Use live regions for results that appear without page reloads.
