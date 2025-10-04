import numpy as np

def market_equilibrium_returns(Sigma: np.ndarray, w_mkt: np.ndarray, delta: float) -> np.ndarray:
    # π = δ Σ w_mkt
    return delta * Sigma @ w_mkt
