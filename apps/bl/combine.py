import numpy as np

def posterior_mean(Sigma: np.ndarray, pi: np.ndarray, P: np.ndarray, q: np.ndarray, Omega: np.ndarray, tau: float) -> np.ndarray:
    # μ* = [(τΣ)^-1 + P'Ω^-1P]^-1 [ (τΣ)^-1 π + P'Ω^-1 q ]
    n = Sigma.shape[0]
    inv_tauSigma = np.linalg.inv(tau * Sigma)
    A = inv_tauSigma + P.T @ np.linalg.inv(Omega) @ P
    b = inv_tauSigma @ pi + P.T @ np.linalg.inv(Omega) @ q
    mu_star = np.linalg.solve(A, b)
    return mu_star
