## 2024-04-18 - Drag and Drop Flickering
**Learning:** In React, `onDragLeave` fires when entering child elements, causing flicker if `isDragging` is simply set to false.
**Action:** Always check `!e.currentTarget.contains(e.relatedTarget as Node)` before disabling drag state.

## 2025-02-17 - Slider Accessibility
**Learning:** Sliders without `aria-label` or `getAriaValueText` are inaccessible to screen reader users. Visual marks also help cognitive load.
**Action:** Always include `aria-label`, `getAriaValueText`, and visual `marks` for critical sliders.

## 2025-05-23 - Custom File Input Accessibility
**Learning:** Default file inputs are ugly, but custom drag-and-drop zones are often inaccessible. Wrapping the zone in a focusable `<label>` makes the entire area interactive for keyboard users and associates it with the hidden input.
**Action:** Use `<label>` as the container for custom file uploads, add `tabIndex="0"`, and handle `onKeyDown` (Enter/Space) to trigger the input click.
