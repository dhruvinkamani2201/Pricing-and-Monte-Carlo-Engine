import asyncio
import websockets
import json
import argparse
import csv
import time
from pathlib import Path

BINANCE_WS = "wss://stream.binance.us:9443/ws/"

async def run(symbol: str, duration: int, out: str):
    symbol_stream = symbol.lower() + "@trade"
    uri = BINANCE_WS + symbol_stream
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    start = time.time()
    with open(out, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["ts", "symbol", "price", "qty"])
        async with websockets.connect(uri, max_size=2**25) as ws:
            while time.time() - start < duration:
                msg = await ws.recv()
                data = json.loads(msg)
                ts = int(data.get("T", time.time()*1000))
                price = data.get("p")
                qty = data.get("q")
                writer.writerow([ts, symbol.upper(), price, qty])

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--symbol", default="BTCUSDT")
    parser.add_argument("--duration", type=int, default=30, help="seconds to run")
    parser.add_argument("--out", default="data/prices.csv")
    args = parser.parse_args()
    asyncio.run(run(args.symbol, args.duration, args.out))

if __name__ == "__main__":
    main()
