import argparse
import os
import sys
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from bot.client import BinanceFuturesClient
from bot.orders import place_order
from bot.exceptions import BinanceAPIException, NetworkException, ValidationException
from bot.logging_config import logger

console = Console()
load_dotenv()


def get_client():
    api_key = os.getenv("API_KEY")
    api_secret = os.getenv("API_SECRET")
    if not api_key or not api_secret:
        console.print(Panel("[bold red]API_KEY or API_SECRET missing in .env![/bold red]", border_style="red"))
        sys.exit(1)
    return BinanceFuturesClient(api_key=api_key, api_secret=api_secret)


def cmd_ping(args):
    console.print("[cyan]Pinging Binance Futures Testnet...[/cyan]")
    try:
        client = get_client()
        with console.status("Connecting..."):
            client.ping()
        console.print("[bold green]✓ Connected successfully! Status: OK[/bold green]")
    except Exception as e:
        console.print(f"[bold red]Failed to connect:[/bold red] {e}")
        sys.exit(1)


def cmd_order(args):
    info = (
        f"Symbol: [bold]{args.symbol}[/bold]  "
        f"Side: [bold]{args.side}[/bold]  "
        f"Type: [bold]{args.order_type}[/bold]  "
        f"Qty: [bold]{args.quantity}[/bold]"
    )
    if args.price:
        info += f"  Price: [bold]{args.price}[/bold]"
    console.print(Panel(info, title="[bold blue]Order Request Summary[/bold blue]", border_style="blue"))

    client = get_client()
    try:
        with console.status("[bold green]Placing order on Binance Testnet..."):
            result = place_order(
                client=client,
                symbol=args.symbol,
                side=args.side,
                order_type=args.order_type,
                quantity=args.quantity,
                price=args.price
            )

        table = Table(title="Order Response", show_header=True, header_style="bold magenta")
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
        table.add_row("Price", str(result.get("price")))
        table.add_row("Time In Force", str(result.get("timeInForce")))
        console.print(table)
        console.print("\n[bold green]SUCCESS: Order successfully placed on Testnet![/bold green]")

    except ValidationException as e:
        console.print(f"\n[bold red]Validation Error:[/bold red] {e}")
        sys.exit(1)
    except BinanceAPIException as e:
        console.print(f"\n[bold red]API Error ({e.status_code}):[/bold red] [{e.error_code}] {e.message}")
        sys.exit(1)
    except NetworkException as e:
        console.print(f"\n[bold red]Network Error:[/bold red] {e}")
        sys.exit(1)
    except Exception as e:
        logger.exception("Unexpected error in CLI")
        console.print(f"\n[bold red]Unexpected Error:[/bold red] {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Binance Futures Testnet Trading Bot",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli.py ping
  python cli.py order --symbol BTCUSDT --side BUY --order-type MARKET --quantity 0.002
  python cli.py order --symbol BTCUSDT --side SELL --order-type LIMIT --quantity 0.002 --price 74000.0
        """
    )
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # ping
    subparsers.add_parser("ping", help="Test connectivity to Binance Futures Testnet")

    # order
    order_parser = subparsers.add_parser("order", help="Place a MARKET or LIMIT order")
    order_parser.add_argument("--symbol", "-s", required=True, help="Symbol e.g. BTCUSDT")
    order_parser.add_argument("--side", required=True, choices=["BUY", "SELL"], help="BUY or SELL")
    order_parser.add_argument("--order-type", "-t", dest="order_type", required=True,
                               choices=["MARKET", "LIMIT"], help="Order type")
    order_parser.add_argument("--quantity", "-q", required=True, type=float, help="Quantity to trade")
    order_parser.add_argument("--price", "-p", type=float, default=None, help="Price (required for LIMIT)")

    args = parser.parse_args()

    if args.command == "ping":
        cmd_ping(args)
    elif args.command == "order":
        cmd_order(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
