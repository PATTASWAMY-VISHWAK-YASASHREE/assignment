## 2024-04-18 - Drag and Drop Flickering
**Learning:** In React, `onDragLeave` fires when entering child elements, causing flicker if `isDragging` is simply set to false.
**Action:** Always check `!e.currentTarget.contains(e.relatedTarget as Node)` before disabling drag state.

## 2025-02-17 - Slider Accessibility
**Learning:** Sliders without `aria-label` or `getAriaValueText` are inaccessible to screen reader users. Visual marks also help cognitive load.
**Action:** Always include `aria-label`, `getAriaValueText`, and visual `marks` for critical sliders.

## 2025-02-18 - Drag and Drop Accessibility
**Learning:** File drag-and-drop zones are often inaccessible to keyboard users. Wrapping the area in a `<label>` with `tabIndex={0}`, `role="button"`, and an `onKeyDown` handler for Enter/Space creates a seamless experience for both mouse and keyboard users.
**Action:** Ensure all custom file uploaders are focusable and trigger file selection via keyboard.
