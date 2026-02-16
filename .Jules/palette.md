## 2024-04-18 - Drag and Drop Flickering
**Learning:** In React, `onDragLeave` fires when entering child elements, causing flicker if `isDragging` is simply set to false.
**Action:** Always check `!e.currentTarget.contains(e.relatedTarget as Node)` before disabling drag state.

## 2025-02-17 - Slider Accessibility
**Learning:** Sliders without `aria-label` or `getAriaValueText` are inaccessible to screen reader users. Visual marks also help cognitive load.
**Action:** Always include `aria-label`, `getAriaValueText`, and visual `marks` for critical sliders.

## 2025-02-18 - Clickable Upload Areas
**Learning:** Dropzones should be fully interactive (click/keyboard). Nesting a button inside a clickable container is invalid HTML.
**Action:** Make the container the primary interactive element (`role="button"`, `tabIndex={0}`) triggering a hidden input via `ref`.
