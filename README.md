Lightweight pricing primitives (Black-Scholes, Monte Carlo, Heston).

- Pricing modules: `pricing/bs.py`, `pricing/monte_carlo.py`, `pricing/heston_mc.py`
- Examples runner: `examples/run_examples.py`
- Unit tests: `tests/test_pricers.py`
- Live market price feeder (WebSocket) that writes CSV: `feed/price_feeder.py`
- Requirements include `pytest` and `websockets`

## Install
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Examples to run
python run.py examples
python run.py feeder --symbol BTCUSDT --duration 30 --out data/prices.csv
python run.py test
