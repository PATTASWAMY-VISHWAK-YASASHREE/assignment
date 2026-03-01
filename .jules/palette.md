## 2024-03-24 - Tooltip on Disabled Buttons
**Learning:** In Material-UI (v6), to display tooltips on disabled buttons, the button must be wrapped in a `<span>`. For keyboard accessibility, this span should have `tabIndex={0}` when the button is disabled, and the tooltip's `disableHoverListener`, `disableFocusListener`, and `disableTouchListener` should be conditionally managed to prevent weird hover states when enabled.
**Action:** Apply this pattern when disabling crucial actions (like "Run Pipeline") to ensure users understand *why* the action is disabled.
