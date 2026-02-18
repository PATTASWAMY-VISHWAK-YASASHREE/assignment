## 2024-04-18 - Drag and Drop Flickering
**Learning:** In React, `onDragLeave` fires when entering child elements, causing flicker if `isDragging` is simply set to false.
**Action:** Always check `!e.currentTarget.contains(e.relatedTarget as Node)` before disabling drag state.

## 2025-02-17 - Slider Accessibility
**Learning:** Sliders without `aria-label` or `getAriaValueText` are inaccessible to screen reader users. Visual marks also help cognitive load.
**Action:** Always include `aria-label`, `getAriaValueText`, and visual `marks` for critical sliders.

## 2026-02-18 - Nested Interactive Elements
**Learning:** Wrapping a button inside a clickable card creates invalid HTML and accessibility issues.
**Action:** Make the outer container the interactive element (role="button", tabIndex=0) and convert the inner button to a visual-only element (component="div", tabIndex=-1, pointerEvents="none").
