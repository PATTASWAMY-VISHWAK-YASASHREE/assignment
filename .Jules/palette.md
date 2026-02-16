## 2024-04-18 - Drag and Drop Flickering
**Learning:** In React, `onDragLeave` fires when entering child elements, causing flicker if `isDragging` is simply set to false.
**Action:** Always check `!e.currentTarget.contains(e.relatedTarget as Node)` before disabling drag state.

## 2025-02-17 - Slider Accessibility
**Learning:** Sliders without `aria-label` or `getAriaValueText` are inaccessible to screen reader users. Visual marks also help cognitive load.
**Action:** Always include `aria-label`, `getAriaValueText`, and visual `marks` for critical sliders.

## 2025-02-18 - Accessible Drag and Drop
**Learning:** Nested interactive elements (button inside clickable div) create invalid semantics. For drop zones, make the container the interactive element (`role="button"`) and hide inner buttons (`aria-hidden="true"`, `tabIndex={-1}`).
**Action:** Use `role="button"`, `tabIndex={0}`, `onKeyDown` on the container, and `component="div"` for inner visual buttons.
