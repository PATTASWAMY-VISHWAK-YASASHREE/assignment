## 2024-10-31 - Semantic Alert Components
**Learning:** Using plain typography for error messages lacks the proper ARIA roles required for screen readers to announce them effectively.
**Action:** Always use semantic alert components like MUI's `<Alert>`, which inherently provide the necessary `role="alert"` and polite `aria-live` attributes.
