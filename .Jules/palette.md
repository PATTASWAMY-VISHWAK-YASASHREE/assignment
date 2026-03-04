## 2024-04-18 - Drag and Drop Flickering
**Learning:** In React, `onDragLeave` fires when entering child elements, causing flicker if `isDragging` is simply set to false.
**Action:** Always check `!e.currentTarget.contains(e.relatedTarget as Node)` before disabling drag state.

## 2025-02-17 - Slider Accessibility
**Learning:** Sliders without `aria-label` or `getAriaValueText` are inaccessible to screen reader users. Visual marks also help cognitive load.
**Action:** Always include `aria-label`, `getAriaValueText`, and visual `marks` for critical sliders.

## 2025-03-04 - Dynamic Live Regions
**Learning:** For conditional, asynchronously loaded text updates (like predictions in `PlaygroundCard`), screen readers require the `aria-live='polite'` and `role='status'` region to be present in the DOM *before* the update occurs.
**Action:** Always render an empty wrapper (e.g., `<Box aria-live="polite" role="status">`) initially, and conditionally render the dynamic content inside it.
