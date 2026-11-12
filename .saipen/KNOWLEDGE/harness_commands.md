# vac34_ae_plugs — canonical harness commands (T-5, SRC-005)

Source of truth: README.md + scripts/manage.py. Verified 2026-11-11 on Windows (node v24.22.1, Python 3.11.9).

- Build bundle: `python build/builder.py --no-tests` → `dist/vac34_AE.jsx` (concatenates src/: Config, AEDom, AudioEngine, TargetResolver, ControllerManager, RecipeRegistry, PresetManager, Diagnostics, Engine, UIBuilder, main; exposes `vac34_*` on `thisObj`/global).
- Full test suite: `python -m unittest discover -s tests -p "test_*.py"` (78 tests). Each builder.py run also re-runs deploy verify (Live Program Files + Mirror `V:\__STORE_V\_AE\install_AEPlugins\...`).
- Elevation: `scripts/install_admin.cmd` (Live install to `C:\Program Files\Adobe\Adobe After Effects 2024\Support Files\Scripts\ScriptUI Panels\vac34_AE.jsx`).
- Unit tests execute the real bundle in `node -e` with hand-built AE mocks (`tests/unit/test_regression_r33_r53.py::run_node_snippet`).
- Baseline at T-5 start: 78/78 PASS on this Windows box (V: present). ZIP baseline hash ea8f3ba7352009e22d554ee4de3933d74b831d744920e6fc441469c047c5145b.
