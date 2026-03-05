## 2024-04-18 - Drag and Drop Flickering
**Learning:** In React, `onDragLeave` fires when entering child elements, causing flicker if `isDragging` is simply set to false.
**Action:** Always check `!e.currentTarget.contains(e.relatedTarget as Node)` before disabling drag state.

## 2025-02-17 - Slider Accessibility
**Learning:** Sliders without `aria-label` or `getAriaValueText` are inaccessible to screen reader users. Visual marks also help cognitive load.
**Action:** Always include `aria-label`, `getAriaValueText`, and visual `marks` for critical sliders.

## 2025-02-18 - Async Async Text Announcement
**Learning:** Conditional, asynchronously loaded text updates (like predictions or errors) require the `aria-live` region to be present in the DOM *before* the update occurs for screen readers to announce it.
**Action:** Always render an empty wrapper initially (e.g. `<Box aria-live="polite" role="status" aria-atomic="true">`), and conditionally render the dynamic content inside it. Use `aria-live="assertive"` for errors (`role="alert"`).
