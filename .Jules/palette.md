## 2024-04-18 - Drag and Drop Flickering
**Learning:** In React, `onDragLeave` fires when entering child elements, causing flicker if `isDragging` is simply set to false.
**Action:** Always check `!e.currentTarget.contains(e.relatedTarget as Node)` before disabling drag state.

## 2025-02-17 - Slider Accessibility
**Learning:** Sliders without `aria-label` or `getAriaValueText` are inaccessible to screen reader users. Visual marks also help cognitive load.
**Action:** Always include `aria-label`, `getAriaValueText`, and visual `marks` for critical sliders.

## 2025-02-18 - Aria-Live Region Rendering & Layout Bugs
**Learning:** For conditional, asynchronously loaded text updates (like predictions or errors), screen readers require the `aria-live` region (e.g., `aria-live='polite'` `role='status'` for info, or `aria-live='assertive'` `role='alert'` for errors) to be present in the DOM *before* the update occurs. However, placing empty persistent wrappers inside flex/stack containers causes blank layout gaps. Furthermore, wrapping MUI `<Alert>` components inside an `aria-live` region creates nested `role="alert"` announcements for screen readers.
**Action:** Always separate the visual states from the screen reader states. Render a separate, empty `<Box sx={visuallyHidden}>` wrapper with the `aria-live` attributes initially, and conditionally update its text content. Ensure the visual alerts also use `aria-hidden="true"` so they aren't double-announced.