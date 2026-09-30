# SecondOrder Homology

This is a bilingual research workspace for testing whether persistent homology helps explain market structure and improves forecasts beyond price and correlation baselines.

Compare the same assets across 20, 60 and 120 observations, inspect persistent features, and review walk-forward results for direction, volatility and stress. You can import a research report generated from your own adjusted-price history and export the results.

The included report uses synthetic prices. It demonstrates the workflow and does not establish a forecasting advantage in real markets.

这是一个中英文研究工作台，用持久同调观察市场结构，并检验它能否在价格和相关性基准之外改善预测。

你可以比较同一组资产在 20、60、120 个观测日下的结构，查看持久特征，以及涨跌方向、波动率和压力状态的滚动样本外检验。也可以导入自己用复权价格数据生成的研究报告，并导出结果。

随附报告使用合成价格，用于演示研究流程，不能证明模型在真实市场中有预测优势。

## Run / 本地运行

Use Node.js 22.13 or later. Python is only needed to generate research reports and run scientific tests.

```bash
npm ci
npm run dev
```

Open http://localhost:3000. The web app uses the committed report and needs no API key or Python service.

网页直接读取仓库里的报告，无需 API key 或 Python 服务。

## Research / 研究方法

See [METHODS.md](METHODS.md) for data requirements, report generation, model definitions and limitations. See [VALIDATION.md](VALIDATION.md) for checks actually completed.

数据要求、报告生成方式、模型定义和局限见 [METHODS.md](METHODS.md)；实际验证记录见 [VALIDATION.md](VALIDATION.md)。

## Release / 发布

Version: **v0.1**

`secondorder-homology-private / v0.1 → secondorder-homology-public / main → Vercel Production`

Private keeps the version history. Public contains the approved release on a single `main` branch. Vercel builds from Public with `npm ci` and `npm run build`.

Private 保留版本历史，Public 只通过 `main` 提供批准发布的版本，Vercel 从 Public 构建网站。
