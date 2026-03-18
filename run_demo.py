import sys
import subprocess
import os

# Use whichever python is available in PATH
PY = sys.executable
CLI = os.path.join(os.path.dirname(__file__), "cli.py")
ENV = {**os.environ}

results = {}

def run_command(label, args):
    print("\n" + "="*55)
    print(f"  {label}")
    print("="*55)
    r = subprocess.run([PY, CLI] + args, capture_output=True, text=True, env=ENV)
    output = r.stdout if r.stdout.strip() else r.stderr
    print(output)
    return {"stdout": r.stdout, "stderr": r.stderr, "code": r.returncode}

# Step 1: PING
results["PING"] = run_command("STEP 1: PING TEST", ["ping"])

# Step 2: MARKET BUY
results["MARKET_BUY"] = run_command(
    "STEP 2: MARKET BUY ORDER (BTCUSDT, Qty=0.002)",
    ["order", "--symbol", "BTCUSDT", "--side", "BUY",
     "--order-type", "MARKET", "--quantity", "0.002"]
)

# Step 3: LIMIT SELL
results["LIMIT_SELL"] = run_command(
    "STEP 3: LIMIT SELL ORDER (BTCUSDT, Qty=0.002, Price=74000)",
    ["order", "--symbol", "BTCUSDT", "--side", "SELL",
     "--order-type", "LIMIT", "--quantity", "0.002", "--price", "74000.0"]
)

# Save output
out_path = os.path.join(os.path.dirname(__file__), "demo_out.txt")
with open(out_path, "w", encoding="utf-8") as f:
    for label, v in results.items():
        f.write(f"\n{'='*55}\n  {label}\n{'='*55}\n")
        f.write(v["stdout"] or v["stderr"])
        f.write(f"\n[EXIT CODE: {v['code']}]\n")

print(f"\n[INFO] Full output saved to {out_path}")
