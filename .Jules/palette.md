## 2024-04-18 - Drag and Drop Flickering
**Learning:** In React, `onDragLeave` fires when entering child elements, causing flicker if `isDragging` is simply set to false.
**Action:** Always check `!e.currentTarget.contains(e.relatedTarget as Node)` before disabling drag state.

## 2025-02-17 - Slider Accessibility
**Learning:** Sliders without `aria-label` or `getAriaValueText` are inaccessible to screen reader users. Visual marks also help cognitive load.
**Action:** Always include `aria-label`, `getAriaValueText`, and visual `marks` for critical sliders.

## 2025-05-19 - Error Accessibility
**Learning:** Colored text (e.g., Typography color="error") is insufficient for error states. Screen readers do not announce color changes.
**Action:** Use `Alert` components (role="alert") for error messages to ensure they are announced and visually distinct.
