import typer
from rich.console import Console
from src.config import settings
from wildberries_python_sdk.client_sync import SyncClient
from src.services.prices import PricesService
from wildberries_python_sdk.exceptions.base import TooManyRequestsError

app = typer.Typer()
console = Console()

@app.command()
def set_price(
    nm_id: int = typer.Option(..., help="NM ID"),
    price: int = typer.Option(..., help="New price"),
    discount: int = typer.Option(..., help="New discount"),
    token: str = typer.Option(None, envvar="WB_TOKEN_PRICES", help="API token"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose logging")
):
    """Set price and discount for a product."""
    if not token:
        token = settings.token_prices
    if not token:
        console.print("[red]Error: API token not provided.[/red]")
        raise typer.Exit(code=1)

    try:
        client = SyncClient(token=token)
        service = PricesService(client)
        
        if verbose:
            console.print(f"Setting price for NM ID {nm_id} to {price} with discount {discount}...")
            
        service.set_prices_and_discounts(nm_id=nm_id, price=price, discount=discount)
        console.print("[green]Price and discount updated successfully.[/green]")
            
    except TooManyRequestsError as e:
        msg = "Rate limit exceeded."
        if e.retry_after:
            msg += f" Please try again in {e.retry_after} seconds."
        console.print(f"[yellow]{msg}[/yellow]")
        raise typer.Exit(code=1)
    except Exception as e:
        if verbose:
            console.print(f"[debug] Exception: {type(e).__name__}: {e}")
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(code=1)
