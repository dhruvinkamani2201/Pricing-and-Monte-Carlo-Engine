import numpy as np

def heston_mc_call(S0, K, r, v0, kappa, theta, xi, rho, T,n_paths=200_000, n_steps=200, seed=1):
    rng = np.random.default_rng(seed)
    dt = T / n_steps
    S = np.full(n_paths, S0, dtype=float)
    v = np.full(n_paths, v0, dtype=float)
    for i in range(n_steps):
        z1 = rng.standard_normal(n_paths)
        z2 = rho * z1 + np.sqrt(1 - rho**2) * rng.standard_normal(n_paths)
        # variance update (full truncation)
        v = v + kappa * (theta - np.maximum(v, 0)) * dt + xi * np.sqrt(np.maximum(v, 0)) * np.sqrt(dt) * z2
        v = np.maximum(v, 0.0)
        S = S * np.exp((r - 0.5 * v) * dt + np.sqrt(v * dt) * z1)
    payoffs = np.maximum(S - K, 0.0)
    price = np.exp(-r * T) * payoffs.mean()
    stderr = np.exp(-r * T) * payoffs.std(ddof=1) / np.sqrt(n_paths)
    return price, stderr
