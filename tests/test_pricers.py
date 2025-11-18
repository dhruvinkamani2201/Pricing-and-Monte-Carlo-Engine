import math
import numpy as np
from pricing.bs import black_scholes_call, black_scholes_put
from pricing.monte_carlo import mc_european_call
from pricing.heston_mc import heston_mc_call

def test_bs_put_call_parity():
    S, K, r, sigma, T = 100.0, 95.0, 0.01, 0.2, 0.5
    call = black_scholes_call(S, K, r, sigma, T)
    put = black_scholes_put(S, K, r, sigma, T)
    # parity: C - P = S - K e^{-rT}
    lhs = call - put
    rhs = S - K * math.exp(-r * T)
    assert abs(lhs - rhs) < 1e-8

def test_mc_vs_bs_consistency():
    S, K, r, sigma, T = 100.0, 100.0, 0.01, 0.2, 1.0
    bs_price = black_scholes_call(S, K, r, sigma, T)
    mc_price, stderr = mc_european_call(S, K, r, sigma, T, n_paths=20000, seed=42)
    # MC should be within ~5 stdev of analytic for small path count
    assert abs(mc_price - bs_price) < 0.05

def test_heston_mc_positive_price():
    S0, K, r = 100.0, 100.0, 0.01
    v0, kappa, theta, xi, rho, T = 0.04, 1.2, 0.04, 0.6, -0.7, 1.0
    price, stderr = heston_mc_call(S0, K, r, v0, kappa, theta, xi, rho, T, n_paths=10000, n_steps=50, seed=1)
    assert price >= 0.0
