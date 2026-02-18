## 2024-04-18 - Drag and Drop Flickering
**Learning:** In React, `onDragLeave` fires when entering child elements, causing flicker if `isDragging` is simply set to false.
**Action:** Always check `!e.currentTarget.contains(e.relatedTarget as Node)` before disabling drag state.

## 2025-02-17 - Slider Accessibility
**Learning:** Sliders without `aria-label` or `getAriaValueText` are inaccessible to screen reader users. Visual marks also help cognitive load.
**Action:** Always include `aria-label`, `getAriaValueText`, and visual `marks` for critical sliders.

## 2026-02-18 - Interactive Containers
**Learning:** Nesting a `<Button>` inside a clickable `Box` (`role="button"`) creates invalid HTML and focus traps.
**Action:** Make the container the button (`tabIndex={0}`, `onKeyDown`) and downgrade inner buttons to visual elements (`component="div"`, `tabIndex={-1}`, `pointerEvents: "none"`).
