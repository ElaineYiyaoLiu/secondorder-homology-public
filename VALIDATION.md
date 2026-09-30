# Validation record

Checked on 2026-09-30 for v0.1.

- All 11 scientific tests passed, covering topology, distance calculations, forward labels, past-only training, future-suffix invariance, input rejection and provider fixtures.
- Report validation passed for the committed 30-asset report and eight malformed inputs.
- DOM interaction checks passed for language and scale switching, H0/H1 selection, asset selection, tabs, target types, calibration, report export, valid/invalid import and demo reset.
- TypeScript checking and the production build passed.
- The production HTTP check returned 200 for the page and the complete research report.
- The downloaded report has Git blob SHA `18d1639e0940d022f6d21f9846a46f5f1e43eb14`, matching the source repository.
- A scan of project source and configuration found no matching private keys or common hard-coded credential patterns.

The local build used `NODE_OPTIONS='--require ./scripts/local-build-shim.cjs'` for the container's unavailable OS RSS query. Vercel uses the normal `npm run build` command.

## Deployment verification

- Private repository: `ElaineYiyaoLiu/secondorder-homology-private`, with only `v0.1`; temporary template mode is disabled.
- Public repository: `ElaineYiyaoLiu/secondorder-homology-public`, with only `main`. All 27 source files match the approved Private snapshot by Git blob SHA.
- Vercel Production successfully built the Public `main` branch using the normal build command.
- Live site: https://secondorder-homology-public.vercel.app/
- Browser checks passed for the complete 30-asset report, Chinese/English, 20D/60D scale switching, H0/H1, Forecast and Backtest views. Desktop geometry layout was visually inspected.
- No application console errors were observed; a browser-extension metadata error was excluded.

## Not verified

- Mobile browser layout was not checked.
- No live market-data provider or real-market forecasting advantage was tested. The default report remains explicitly synthetic.

## Reproduce

```bash
npm ci
python -m venv .venv
.venv/bin/python -m pip install -r python/requirements.txt
HOMOLOGY_PYTHON=.venv/bin/python npm test
npm run test:report
npm run test:ui
npm run typecheck
npm run build
npm run test:http
```
