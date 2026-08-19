# MediCheck Repository Guidance

- UI/UX modernization is the current priority. Preserve the existing clinic workflow: check-in or register, manage the queue, select the next patient, document symptoms/diagnosis/prescriptions, and review the summary/history.
- Fix backend bugs when they block UI work or materially affect reliability, but avoid broad rewrites without a clear reason.
- Use `UserRequest.py` as the preferred boundary between Tkinter code and backend/database code. Do not add direct UI calls into formulas, pipeline objects, or SQL helpers.
- Build reusable Tkinter components and shared styling instead of duplicating widget setup. Gradually replace unnecessary `Toplevel` chains with coordinated views in one application shell.
- Present patients, queues, visits, and histories as structured fields, cards, or tables—not raw `Text`/`repr` output.
- Treat current code as the source of truth when README or other documentation disagrees; record or deliberately resolve discrepancies.
- Prefer cohesive feature changes over many tiny edits. Avoid unrelated cleanup and do not repeatedly inspect files that have not changed.
- Validate the smallest relevant surface (focused unit checks, compile/import checks, or a specific manual UI path) instead of repeatedly running broad test suites.
- Do not commit or push unless the user explicitly requests it.
- At task completion, report files changed, implementation summary, validation performed, blockers, and the recommended next step.
