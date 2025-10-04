def render_report(perf: dict) -> str:
    return f"Sharpe: {perf.get('sharpe', 0):.3f}"
