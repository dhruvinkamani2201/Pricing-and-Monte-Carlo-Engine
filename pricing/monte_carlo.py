import numpy as np

def mc_european_call(S0, K, r, sigma, T, n_paths=200_000, n_steps=1, antithetic=True, seed=0):
    rng = np.random.default_rng(seed)
    dt = T / n_steps
    drift = (r - 0.5 * sigma**2) * dt
    vol = sigma * np.sqrt(dt)
    # Simulate in log-space
    if antithetic:
        half = n_paths // 2
        Z = rng.standard_normal((half, n_steps))
        Z = np.vstack([Z, -Z])
    else:
        Z = rng.standard_normal((n_paths, n_steps))
    logS = np.log(S0) + np.cumsum(drift + vol * Z, axis=1)
    ST = np.exp(logS[:, -1])
    payoffs = np.maximum(ST - K, 0.0)
    price = np.exp(-r * T) * payoffs.mean()
    stderr = np.exp(-r * T) * payoffs.std(ddof=1) / np.sqrt(n_paths)
    return price, stderr
