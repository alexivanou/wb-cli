import typer
from rich.console import Console
from rich.table import Table
from typing import List
from src.config import settings
from wildberries_python_sdk.client_sync import SyncClient
from src.services.products import ProductsService
from wildberries_python_sdk.exceptions.base import TooManyRequestsError

app = typer.Typer()
console = Console()

@app.command()
def get_products(
    limit: int = typer.Option(10, help="Number of items to return"),
    offset: int = typer.Option(0, help="Offset for pagination"),
    token: str = typer.Option(None, envvar="WB_TOKEN_PRODUCTS", help="API token"),
    json_output: bool = typer.Option(False, "--json", help="Output in JSON format"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose logging")
):
    """Get list of seller products."""
    if not token:
        token = settings.token_products
    if not token:
        console.print("[red]Error: API token not provided.[/red]")
        raise typer.Exit(code=1)

    try:
        client = SyncClient(token=token)
        service = ProductsService(client)
        
        if verbose:
            console.print(f"Fetching products (limit={limit}, offset={offset})...")
            
        products = service.get_products(limit=limit, offset=offset)

        if json_output:
            console.print([p.model_dump_json() for p in products])
        else:
            table = Table(title="Seller Products")
            table.add_column("NM ID", style="cyan")
            table.add_column("Vendor Code", style="magenta")
            table.add_column("Subject", style="green")

            for p in products:
                table.add_row(str(p.nm_id), p.vendor_code, p.subject_name)
            
            console.print(table)
            
    except TooManyRequestsError as e:
        msg = "Rate limit exceeded."
        if e.retry_after:
            msg += f" Please try again in {e.retry_after} seconds."
        console.print(f"[yellow]{msg}[/yellow]")
        raise typer.Exit(code=1)
    except Exception as e:
        if verbose:
            console.print(f"[debug] Exception: {type(e).__name__}: {e}")
            if hasattr(e, 'raw_response') and e.raw_response:
                console.print(f"[debug] Raw response: {e.raw_response}")
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(code=1)
