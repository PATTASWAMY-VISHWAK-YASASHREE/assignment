## 2024-04-18 - Drag and Drop Flickering
**Learning:** In React, `onDragLeave` fires when entering child elements, causing flicker if `isDragging` is simply set to false.
**Action:** Always check `!e.currentTarget.contains(e.relatedTarget as Node)` before disabling drag state.

## 2025-02-17 - Slider Accessibility
**Learning:** Sliders without `aria-label` or `getAriaValueText` are inaccessible to screen reader users. Visual marks also help cognitive load.
**Action:** Always include `aria-label`, `getAriaValueText`, and visual `marks` for critical sliders.

## 2025-02-24 - Interactive Drop Zones
**Learning:** Drop zones that are not keyboard accessible exclude users who cannot drag and drop. Nested interactive controls (button inside clickable div) cause accessibility issues.
**Action:** Make the container the primary interactive element (`role="button"`, `tabIndex={0}`, `onKeyDown`) and ensure inner buttons are purely visual (`tabIndex={-1}`, `aria-hidden="true"`).
