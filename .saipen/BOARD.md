# Board

<!-- Ticket shape is RFC § 1.2's, exactly: a checkbox, the T-### id, a
     description, then only the fields that apply, space-pipe separated.
     Shown here WITHOUT its leading "- " on purpose (see below):

       [ ] T-001 short description | verify: pytest -q

     Other legal fields (RFC § 1.2): the dependency one, taking a
     comma-separated list of T-### this ticket waits on; owner and
     claim_time for claims (§ 1.4); blocker for facts + dead ends; verify as
     shown above. Named rather than shown here on purpose -- see below.

     A real line starts with "- ". Checkbox: [ ] open, [/] in progress
     (## DOING), [x] done (## DONE). A status change MOVES the line between
     sections -- cut and paste, never copy, or the same id ends up under two
     headings. All four headings below are required, even while empty.

     Why the example is de-fanged: neither validator skips HTML comments, so
     anything ticket-shaped in here is read as a real ticket on a brand-new,
     untouched board. Two separate traps, both hit for real while writing
     this very file: a full checkbox line parses as a live ticket, and the
     dependency field followed by an id is flagged as a dangling reference
     even without a leading dash -- tests/validate.sh scans for that field
     across the whole file, not only ticket lines, making it stricter here
     than tools/validate.py. So: no leading dash on any example, and never
     write that field name next to a concrete id anywhere in this file. -->

## DOING

## TODO

## DONE
- [x] T-7 [P2] T-7: pinned target integrity, shared master lifecycle, ScriptUI acceptance, Glow Threshold P0 campaign per SAIHANDOFF | verify: the requested change is present and demonstrated against the user own description of it | request_witness: model_supplied | source_receipts: SRC-007 | owner: saipen | claim_time: 2026-11-12T04:58:21Z | closure_mode: cohort | closure_cohort: C-7 | closure_paths: dist/vac34_AE.jsx
- [x] T-6 [P2] P0 UI/UX recovery vac34_AE: visible apply results, scrollable fixed-footer panel, comp/target pin, audio source validation, glow threshold acceptance, build... | verify: the requested change is present and demonstrated against the user own description of it | request_witness: model_supplied | source_receipts: SRC-006 | owner: saipen | claim_time: 2026-11-12T00:31:35Z | closure_mode: own_patch | publication_state: pending
- [x] T-5 [P2] vac34_AE P0: expression integrity, property identity, dim compatibility, audio identity, regressions R54-R70, release pipeline | verify: the requested change is present and demonstrated against the user own description of it | request_witness: model_supplied | source_receipts: SRC-005 | owner: saipen | claim_time: 2026-11-11T21:58:43Z | closure_mode: own_patch | publication_state: pending
- [x] T-4 [P2] # SAIHANDOFF — VAC34_AE P0: REAL AE PROPERTY INVALIDATION, NON-DESTRUCTIVE TARGETING AND LIVE INSTALLATION | verify: the requested change is present and demonstrated against the user own description of it | request_witness: model_supplied | source_receipts: SRC-004 | owner: saipen | claim_time: 2026-11-07T18:55:01Z | closure_mode: own_patch | publication_state: pending
- [x] T-3 [P2] @[SAIHANDOFF_VAC34_AE_P0_RECOVERY,_ENGINE_INTEGRITY_AND_HONEST_RELEASE_20261107_144351_d0ca3cfb.md] | verify: the requested change is present and demonstrated against the user own description of it | request_witness: model_supplied | source_receipts: SRC-003 | owner: saipen | claim_time: 2026-11-07T12:49:13Z | closure_mode: own_patch | publication_state: pending
- [x] T-2 [P2] # SAIHANDOFF — vac34_AE v0.0.1: FORENSIC RECOVERY + P0 HARDENING | verify: the requested change is present and demonstrated against the user own description of it | request_witness: model_supplied | source_receipts: SRC-002 | owner: saipen | claim_time: 2026-11-07T12:32:35Z | claim_session: a1fbbdc22c9f48f22ca6820ddd6f9509 | closure_mode: own_patch | publication_state: pending
- [x] T-1 [P2] # SAIHANDOFF — VAC34 AFTER EFFECTS MASTER EXPRESSIONS STUDIO | verify: the requested change is present and demonstrated against the user own description of it | request_witness: model_supplied | source_receipts: SRC-001 | owner: saipen | claim_time: 2026-11-07T12:05:38Z | closure_mode: own_patch | publication_state: pending

## BLOCKED
