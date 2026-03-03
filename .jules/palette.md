## 2025-02-13 - MUI Custom Dropzone Accessibility
**Learning:** Custom drag-and-drop zones built with MUI `<Box>` lack native accessibility. Simply adding an `<input type="file">` inside isn't enough for keyboard users.
**Action:** Always make custom dropzones accessible by adding `role="button"`, `tabIndex={0}`, an explicit `aria-label`, an `onKeyDown` handler (for Enter/Space) to trigger the hidden file input, and `:focus-visible` styling (e.g., `outline: "2px solid"`) to the container `<Box>`.
