import numpy as np
def sharpe(returns, rf=0.0):
    r = np.asarray(returns)
    return (r.mean() - rf) / (r.std(ddof=1) + 1e-9)
