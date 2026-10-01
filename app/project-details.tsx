'use client';

export default function ProjectDetails({ zh }: { zh: boolean }) {
  return (
    <details className="project-details" onKeyDown={event => {
      if (event.key === 'Escape') {
        event.currentTarget.removeAttribute('open');
        event.currentTarget.querySelector('summary')?.focus();
      }
    }}>
      <summary><span>{zh ? '项目详情' : 'Project details'}</span><span className="details-chevron" aria-hidden="true">⌄</span></summary>
      <section className="project-details-panel" aria-label={zh ? 'Homology 项目详情' : 'Homology project details'}>
        <h2>Homology</h2>
        {zh ? <p>这个模型把几十只股票的滚动相关矩阵转成 <strong>correlation distance matrix</strong>，再用<strong>持续同调（persistent homology）</strong>捕捉 H₀ 和 H₁ 拓扑结构随时间发生的变化，并用 <strong>Wasserstein-2 distance</strong> 衡量这些结构移动的速度和加速度。最后通过 <strong>Logistic Regression、Ridge Regression 和 walk-forward backtest</strong>，检验这些拓扑变化能不能帮助我们更早看见个股方向、波动和整个市场压力的变化。</p> : <p>This model converts rolling correlations across dozens of stocks into <strong>correlation distance matrices</strong>, then uses <strong>persistent homology</strong> to track changes in H₀ and H₁ topological structures over time. <strong>Wasserstein-2 distance</strong> measures how quickly those structures are moving, while <strong>Logistic Regression, Ridge Regression, and walk-forward backtesting</strong> test whether these changes contain earlier information about stock direction, volatility, and broader market stress.</p>}
      </section>
    </details>
  );
}
