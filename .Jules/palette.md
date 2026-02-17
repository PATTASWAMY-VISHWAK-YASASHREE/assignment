## 2024-04-18 - Drag and Drop Flickering
**Learning:** In React, `onDragLeave` fires when entering child elements, causing flicker if `isDragging` is simply set to false.
**Action:** Always check `!e.currentTarget.contains(e.relatedTarget as Node)` before disabling drag state.

## 2025-02-17 - Slider Accessibility
**Learning:** Sliders without `aria-label` or `getAriaValueText` are inaccessible to screen reader users. Visual marks also help cognitive load.
**Action:** Always include `aria-label`, `getAriaValueText`, and visual `marks` for critical sliders.

## 2026-02-17 - Accessible File Upload
**Learning:** File inputs hidden inside buttons are not enough; the entire drop zone should be interactive (clickable, focusable) for better usability and accessibility. `aria-describedby` is crucial for linking file constraints.
**Action:** Make drop zones `role="button"` with `tabIndex={0}`, handle `onClick` and `onKeyDown` to trigger the hidden input, and use `aria-describedby` for helper text.
