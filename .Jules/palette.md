## 2024-04-18 - Drag and Drop Flickering
**Learning:** In React, `onDragLeave` fires when entering child elements, causing flicker if `isDragging` is simply set to false.
**Action:** Always check `!e.currentTarget.contains(e.relatedTarget as Node)` before disabling drag state.

## 2025-02-17 - Slider Accessibility
**Learning:** Sliders without `aria-label` or `getAriaValueText` are inaccessible to screen reader users. Visual marks also help cognitive load.
**Action:** Always include `aria-label`, `getAriaValueText`, and visual `marks` for critical sliders.

## 2025-03-07 - Screen Reader Announcements in React Layouts
**Learning:** Adding dynamic text directly to conditional UI components (like alerts or predictions) that mount/unmount inside Flexbox/Stack layouts causes missing or duplicated screen reader announcements. Screen readers require the `aria-live` region to exist in the DOM *before* the message is updated.
**Action:** Render a separate, permanent, visually hidden `<Box>` element with `aria-live="polite"` or `aria-live="assertive"` to mirror the dynamic text, and add `aria-hidden="true"` to the conditionally rendered visible UI elements to avoid duplicate announcements.
