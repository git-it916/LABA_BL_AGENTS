import numpy as np
from scipy.optimize import minimize

def optimal_weights(mu: np.ndarray, Sigma: np.ndarray, lb=-0.05, ub=0.10):
    n = len(mu)
    x0 = np.ones(n) / n
    bounds = [(lb, ub)] * n
    cons = ({"type": "eq", "fun": lambda w: np.sum(w) - 1.0},)

    def neg_utility(w):
        # maximize w' mu - 0.5 w' Σ w  (equiv. minimize negative)
        return - (w @ mu - 0.5 * (w @ Sigma @ w))

    res = minimize(neg_utility, x0, bounds=bounds, constraints=cons, method="SLSQP", options={"maxiter": 500})
    if not res.success:
        raise RuntimeError(res.message)
    return res.x
