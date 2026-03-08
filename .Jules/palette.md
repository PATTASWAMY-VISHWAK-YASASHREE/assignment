## 2024-04-18 - Drag and Drop Flickering
**Learning:** In React, `onDragLeave` fires when entering child elements, causing flicker if `isDragging` is simply set to false.
**Action:** Always check `!e.currentTarget.contains(e.relatedTarget as Node)` before disabling drag state.

## 2025-02-17 - Slider Accessibility
**Learning:** Sliders without `aria-label` or `getAriaValueText` are inaccessible to screen reader users. Visual marks also help cognitive load.
**Action:** Always include `aria-label`, `getAriaValueText`, and visual `marks` for critical sliders.

## 2025-02-23 - Disabled Button Tooltips in MUI
**Learning:** In Material-UI (v6), natively disabled buttons are removed from the focus order, making tooltips attached directly to them inaccessible to keyboard/screen reader users.
**Action:** Always wrap disabled buttons in a `<span>` with `tabIndex={0}` (conditionally applied only when disabled). Conditionally disable the Tooltip listeners (`disableHoverListener`, `disableFocusListener`, `disableTouchListener`) when the button is *not* disabled to avoid double-triggers or redundant tooltips.