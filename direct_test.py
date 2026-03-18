#!/usr/bin/env python3
"""Direct test script to verify trading bot functionality without CLI parsing issues."""

import os
import sys
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# Add bot package to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bot.client import BinanceFuturesClient
from bot.orders import place_order
from bot.exceptions import BinanceAPIException, NetworkException, ValidationException
from bot.logging_config import logger

console = Console()
load_dotenv()

def main():
    api_key = os.getenv("API_KEY")
    api_secret = os.getenv("API_SECRET")
    
    if not api_key or not api_secret:
        console.print("[bold red]ERROR: API_KEY or API_SECRET missing in .env![/bold red]")
        return False
    
    client = BinanceFuturesClient(api_key=api_key, api_secret=api_secret)
    test_results = []
    
    # TEST 1: CONNECTIVITY (PING)
    console.print("\n[bold cyan]TEST 1: CONNECTIVITY[/bold cyan]")
    try:
        result = client.ping()
        console.print("[bold green]✓ PING SUCCESS[/bold green] - Connected to Binance Testnet")
        test_results.append(("Connectivity (Ping)", True))
    except Exception as e:
        console.print(f"[bold red]✗ PING FAILED: {e}[/bold red]")
        test_results.append(("Connectivity (Ping)", False))
        return False
    
    # TEST 2: MARKET BUY ORDER
    console.print("\n[bold cyan]TEST 2: MARKET BUY ORDER[/bold cyan]")
    try:
        info = "[bold]Market Order Summary[/bold]\nSymbol: BTCUSDT | Side: BUY | Type: MARKET | Qty: 0.002"
        console.print(Panel(info, border_style="blue"))
        
        result = place_order(
            client=client,
            symbol="BTCUSDT",
            side="BUY",
            order_type="MARKET",
            quantity=0.002
        )
        
        table = Table(title="Market Order Execution Details", show_header=True, header_style="bold magenta")
        table.add_column("Field", style="cyan", no_wrap=True)
        table.add_column("Value", style="green")
        table.add_row("Order ID", str(result.get("orderId")))
        table.add_row("Symbol", str(result.get("symbol")))
        table.add_row("Status", str(result.get("status")))
        table.add_row("Side", str(result.get("side")))
        table.add_row("Type", str(result.get("origType")))
        table.add_row("Orig Qty", str(result.get("origQty")))
        table.add_row("Executed Qty", str(result.get("executedQty")))
        table.add_row("Avg Price", str(result.get("avgPrice")))
        
        console.print(table)
        console.print("[bold green]✓ MARKET ORDER PLACED SUCCESSFULLY[/bold green]")
        test_results.append(("Market Order", True))
    except Exception as e:
        console.print(f"[bold red]✗ MARKET ORDER FAILED: {e}[/bold red]")
        test_results.append(("Market Order", False))
    
    # TEST 3: LIMIT SELL ORDER
    console.print("\n[bold cyan]TEST 3: LIMIT SELL ORDER[/bold cyan]")
    try:
        info = "[bold]Limit Order Summary[/bold]\nSymbol: BTCUSDT | Side: SELL | Type: LIMIT | Qty: 0.002 | Price: 90000.0"
        console.print(Panel(info, border_style="blue"))
        
        result = place_order(
            client=client,
            symbol="BTCUSDT",
            side="SELL",
            order_type="LIMIT",
            quantity=0.002,
            price=90000.0
        )
        
        table = Table(title="Limit Order Execution Details", show_header=True, header_style="bold magenta")
        table.add_column("Field", style="cyan", no_wrap=True)
        table.add_column("Value", style="green")
        table.add_row("Order ID", str(result.get("orderId")))
        table.add_row("Symbol", str(result.get("symbol")))
        table.add_row("Status", str(result.get("status")))
        table.add_row("Side", str(result.get("side")))
        table.add_row("Type", str(result.get("origType")))
        table.add_row("Price", str(result.get("price")))
        table.add_row("Orig Qty", str(result.get("origQty")))
        table.add_row("Executed Qty", str(result.get("executedQty")))
        table.add_row("Time In Force", str(result.get("timeInForce")))
        
        console.print(table)
        console.print("[bold green]✓ LIMIT ORDER PLACED SUCCESSFULLY[/bold green]")
        test_results.append(("Limit Order", True))
    except Exception as e:
        console.print(f"[bold red]✗ LIMIT ORDER FAILED: {e}[/bold red]")
        test_results.append(("Limit Order", False))
    
    # TEST 4: INPUT VALIDATION (should fail)
    console.print("\n[bold cyan]TEST 4: INPUT VALIDATION[/bold cyan]")
    try:
        # This should fail - negative quantity
        result = place_order(
            client=client,
            symbol="BTCUSDT",
            side="BUY",
            order_type="MARKET",
            quantity=-0.001
        )
        console.print("[bold red]✗ VALIDATION FAILED - Should have rejected negative quantity[/bold red]")
        test_results.append(("Input Validation", False))
    except ValidationException as e:
        console.print(f"[bold green]✓ VALIDATION SUCCESS[/bold green] - Correctly rejected invalid input: {e}")
        test_results.append(("Input Validation", True))
    except Exception as e:
        console.print(f"[bold red]✗ VALIDATION TEST ERROR: {e}[/bold red]")
        test_results.append(("Input Validation", False))
    
    # TEST 5: LIMIT ORDER WITHOUT PRICE (should fail)
    console.print("\n[bold cyan]TEST 5: LIMIT ORDER VALIDATION[/bold cyan]")
    try:
        # This should fail - LIMIT without price
        result = place_order(
            client=client,
            symbol="BTCUSDT",
            side="BUY",
            order_type="LIMIT",
            quantity=0.001,
            price=None
        )
        console.print("[bold red]✗ LIMIT VALIDATION FAILED - Should have rejected LIMIT without price[/bold red]")
        test_results.append(("Limit Order Validation", False))
    except ValidationException as e:
        console.print(f"[bold green]✓ LIMIT VALIDATION SUCCESS[/bold green] - Correctly rejected LIMIT without price: {e}")
        test_results.append(("Limit Order Validation", True))
    except Exception as e:
        console.print(f"[bold red]✗ LIMIT VALIDATION ERROR: {e}[/bold red]")
        test_results.append(("Limit Order Validation", False))
    
    # SUMMARY
    console.print("\n" + "="*60)
    console.print("[bold]TEST SUMMARY[/bold]")
    console.print("="*60)
    
    summary_table = Table(show_header=True, header_style="bold")
    summary_table.add_column("Test Name", style="cyan")
    summary_table.add_column("Result", style="green")
    
    all_passed = True
    for test_name, passed in test_results:
        status = "[bold green]PASSED[/bold green]" if passed else "[bold red]FAILED[/bold red]"
        summary_table.add_row(test_name, status)
        if not passed:
            all_passed = False
    
    console.print(summary_table)
    console.print("="*60)
    
    if all_passed:
        console.print("\n[bold green]✓ ALL TESTS PASSED![/bold green]")
    else:
        console.print("\n[bold red]✗ SOME TESTS FAILED[/bold red]")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
