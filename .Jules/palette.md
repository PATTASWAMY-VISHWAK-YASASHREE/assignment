## 2024-04-18 - Drag and Drop Flickering
**Learning:** In React, `onDragLeave` fires when entering child elements, causing flicker if `isDragging` is simply set to false.
**Action:** Always check `!e.currentTarget.contains(e.relatedTarget as Node)` before disabling drag state.

## 2025-02-17 - Slider Accessibility
**Learning:** Sliders without `aria-label` or `getAriaValueText` are inaccessible to screen reader users. Visual marks also help cognitive load.
**Action:** Always include `aria-label`, `getAriaValueText`, and visual `marks` for critical sliders.
## 2024-03-08 - Accessible Dynamic Text in Flexbox/Stack Layouts
**Learning:** For conditional, asynchronously loaded text updates (like errors or predictions), rendering `aria-live` directly on components like `<Alert>` inside MUI Flexbox/Stack layouts creates layout bugs and causes double announcements by screen readers. Furthermore, importing `visuallyHidden` from `@mui/utils` or `@mui/system` breaks Vite builds in this project.
**Action:** Render a separate, permanent `<Box>` at the top of the component to mirror the dynamic text with `aria-live="polite"` and manual visually hidden CSS properties in the `sx` prop. Apply `aria-hidden="true"` to the actual visible UI elements to prevent duplicate reading.
