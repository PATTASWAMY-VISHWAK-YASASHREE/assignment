## 2024-04-18 - Drag and Drop Flickering
**Learning:** In React, `onDragLeave` fires when entering child elements, causing flicker if `isDragging` is simply set to false.
**Action:** Always check `!e.currentTarget.contains(e.relatedTarget as Node)` before disabling drag state.

## 2025-02-17 - Slider Accessibility
**Learning:** Sliders without `aria-label` or `getAriaValueText` are inaccessible to screen reader users. Visual marks also help cognitive load.
**Action:** Always include `aria-label`, `getAriaValueText`, and visual `marks` for critical sliders.

## 2025-02-18 - File Upload Accessibility
**Learning:** Large drag-and-drop zones are often not keyboard accessible. Users must tab to a tiny 'Select File' button instead of using the whole area.
**Action:** Make the entire drop container interactive with `role='button'`, `tabIndex={0}`, and click/keydown handlers that trigger a hidden file input.
