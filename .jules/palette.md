# Palette's Journal - Critical UX/A11y Learnings

This journal tracks critical accessibility and UX patterns discovered while working on the codebase.

## Entries

## 2026-02-25 - Client-Side Validation Feedback
**Learning:** Found critical pattern where user inputs (JSON) are only validated on submission (backend error), creating friction.
**Action:** Implement `onBlur` validation for complex inputs to provide immediate, actionable feedback without waiting for server response.
