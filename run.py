import sys
import subprocess
import argparse
from pathlib import Path

ROOT = Path(__file__).parent

def run_examples():
    subprocess.check_call([sys.executable, str(ROOT / "examples" / "run_examples.py")])

def run_feeder(symbol="BTCUSDT", duration=30, out="data/prices.csv"):
    feeder = ROOT / "feed" / "price_feeder.py"
    subprocess.check_call([sys.executable, str(feeder), "--symbol", symbol, "--duration", str(duration), "--out", out])

def run_tests():
    subprocess.check_call([sys.executable, "-m", "pytest", "-q"])

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("cmd", choices=["examples","feeder","test"])
    parser.add_argument("--symbol", default="BTCUSDT")
    parser.add_argument("--duration", type=int, default=30)
    parser.add_argument("--out", default="data/prices.csv")
    args = parser.parse_args()

    if args.cmd == "examples":
        run_examples()
    elif args.cmd == "feeder":
        run_feeder(symbol=args.symbol, duration=args.duration, out=args.out)
    elif args.cmd == "test":
        run_tests()

if __name__ == "__main__":
    main()