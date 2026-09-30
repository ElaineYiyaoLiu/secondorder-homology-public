# Methods and reproducibility

A bilingual, three-column research workspace asking whether persistent homology improves held-out forecasts relative to specified price and correlation baselines. It does not presume that PH has a predictive edge. The included data are **synthetic, invented prices**, ending 2025-06-30. Every view labels them. Their model outputs are not evidence about real stock markets.

## Run

Node >=22.13 and Python 3.11+ recommended.

```bash
npm ci
python -m venv .venv
.venv/bin/python -m pip install -r python/requirements.txt
npm test
npm run typecheck
npm run build
npm start
```

In this restricted local container, Node’s OS RSS query throws `ENOENT`. The verified local build uses `NODE_OPTIONS='--require ./scripts/local-build-shim.cjs' npm run build`. The shim uses V8 heap statistics only when that OS query fails, and is not part of the Vercel build command.

Open http://localhost:3000. `npm run dev` is also available. A reproducible demo report is committed, so the web app does not require Python or API credentials to run. `npm run research:demo` regenerates it. `HOMOLOGY_PYTHON` can override the Python executable used by npm scripts (Windows users may use `.venv/Scripts/python.exe`).

## What is implemented

- Fixed 30-asset demo universe; CSV pipeline supports 30–50 assets.
- Aligned daily log returns; 20/60/120-observation Pearson correlation distance `sqrt(2*(1-rho))`. No pairwise deletion, filling, or nearest-PSD repair.
- Complete Vietoris–Rips H0/H1 persistent homology over F2 using Ripser. All triangles are filled at their longest edge. H2 is not computed. The essential H0 class is excluded, not arbitrarily capped.
- Energy, total/maximum persistence, entropy, exact Euclidean-ground W2 with diagonal matching, velocity acceleration and first/second energy differences, at each dimension and scale. These are discrete changes per observation.
- Filtration slider, selectable graph nodes, H0/H1 diagram with point details, first persistence landscape, common-color-scale velocity timeline, descriptive historical percentiles.
- Per-asset 5-session direction, 20-session annualized RMS volatility and a 20-session stress target.
- 3 nested models: 6 price features; 21 price/correlation features; 69 price/correlation/PH features. Correlation controls include mean, dispersion, leading eigenvalue share, participation ratio and matrix-change norm at each scale.
- Past-only StandardScaler and fixed regularized logistic regression (`C=.05`) / ridge regression of log volatility (`alpha=50`). No test-driven hyperparameter selection.
- Expanding-window walk-forward with >=252 matured training samples, 20-observation refits, strict `labelEnd < blockOrigin`, identical eligible origins for the three models within each task. No random split.
- Brier/log-loss/balanced accuracy/AUC or variance QLIKE/MAE/RMSE, held-out probability bins, full fold and prediction exports.
- Paired circular-block bootstrap of correlation-minus-PH loss: 1,000 samples, 20-session blocks. Positive loss difference means PH improves. Zero-crossing intervals are labeled inconclusive; negative results remain visible.
- Optional Twelve Data offline provider using an environment secret, fail-closed behavior and documented `adjust=all`. No provider request occurs on browser load.

## Real-history research

Provide a CSV with first column `date`, then **30–50 uniquely named adjusted-close or total-return index columns**. Require >=600 completed daily observations, exact date alignment, positive finite values, no duplicate/unsorted dates, no constant rolling windows and no daily moves beyond 80%. This last bound is an intentional data-quality guard and may reject genuine extreme returns; investigate rather than silently clipping. Today's New York session and future observations are rejected. Calendar dates are not asserted to be exchange sessions: the user/vendor must supply the correct completed-session calendar.

```bash
.venv/bin/python python/research.py \
  --csv data/prices.csv \
  --source 'Vendor / adjustments / universe policy' \
  --output research.json
```

Import `research.json` using **Import research report**. The browser validates structure and supported method configuration. Imported files stay in browser memory and are lost on reload. Import validation is not cryptographic verification of the raw data or the user's provenance claim. Export downloads preserve the full report. To publish a real report as the default, replace `public/data/demo.json` with generated output; the UI reads the report's source type, not the filename. Do not publish vendor data without appropriate rights.

To download the same default 30 assets using your local Twelve Data account:

```bash
# Configure TWELVE_DATA_API_KEY outside source control, in your local environment.
.venv/bin/python python/download_prices.py --output data/prices.csv
```

The adapter requests 2,000 daily observations per symbol, with an 8-second inter-request pause configurable for the account's quota. It checks complete aligned observations and writes provenance next to the CSV. It does not substitute synthetic prices, drop failing tickers, or silently fill/drop dates. API plan, adjustments, data licensing and actual live-provider behavior must be verified with a real account. `--targets NVDA SPY` can limit model fitting while retaining the complete geometry universe.

## Methods and limits

Direction labels use `sum(log_returns[t+1:t+6]) > 0`. Volatility is `sqrt(252*mean(log_returns[t+1:t+21]^2))`; it is RMS, not demeaned sample standard deviation. Stress labels use each fold's **training future-volatility** 80th percentile, so the stress definition is training-adaptive. The first two PH history rows are discarded to establish derivative history. Predictions are made at completed-session close; training labels must already be complete strictly before that close. The latest forecast uses all eligible matured rows with the same conservative availability rule.

Correlation-distance PH is a deterministic function of the **full correlation matrix**. A gain over a limited summary baseline does not prove information outside correlation, nonlinear dependence, or a causal mechanism. The graph uses a fixed circular layout, not a distance-preserving embedding. It shows the 1-skeleton and reports the number of filled triangles; a visible graph cycle is not necessarily an H1 feature, and drawn edges do not identify representative persistent cycles. All targets in the fixed universe share one market geometry; target-specific price features and fitted models differ.

Joint 20-observation block shuffling is included as a covariance-preserving diagnostic. It changes rolling matrices and is **not a completed forecasting surrogate significance test**. Bootstrap intervals are sample/specification-conditional, descriptive, and uncorrected for multiple targets or assets. Overlapping labels make observation count different from independent sample count. Real fixed-current-stock samples have survivorship bias without point-in-time universes, delistings and properly vintaged vendor data. The app makes no trading profit or crash-warning claim and does not fabricate transaction-cost simulations.

## Deployment

The frontend is a standard Next.js App Router app. Research is offline precomputation: no Python service, database, secrets or expensive PH calculation is required in Vercel requests.

Release flow: Private version branch → Public `main` → Vercel Production. The checked-in `vercel.json` uses `npm ci` and `npm run build`. Verify the deployed page, synthetic-data status, language controls, diagram, report import/export and backtest tabs after every production deployment.

GitHub Actions runs Python research tests, TypeScript report-schema tests and the production build on push/PR. The demonstration artifact includes its data SHA-256, seeds, model settings, fold audit and package versions. It contains raw per-origin predictions, not manually chosen headline numbers.

## Validation

Run `npm test`, `npm run test:report`, `npm run test:ui`, `npm run typecheck`, `npm run build`, then `npm run test:http`. Scientific tests cover the filled-triangle and square-loop examples, W2 diagonal assignment, metric validity, forward-label boundaries, scaler training-only fitting, future-suffix invariance of both features and held-out predictions, data rejection and surrogate covariance preservation. Browser QA is described in `VALIDATION.md` after execution.

References: [Ripser](https://ripser.scikit-tda.org/en/latest/reference/stubs/ripser.ripser.html), [scikit-learn leakage guidance](https://scikit-learn.org/stable/common_pitfalls.html#data-leakage), [Twelve Data API](https://twelvedata.com/docs).
