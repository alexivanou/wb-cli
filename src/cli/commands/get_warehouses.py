import typer
from rich.console import Console
from rich.table import Table
from src.config import settings
from wildberries_python_sdk.client_sync import SyncClient
from src.services.warehouse import WarehouseService
from wildberries_python_sdk.exceptions.base import TooManyRequestsError

app = typer.Typer()
console = Console()

@app.command()
def get_warehouses(
    token: str = typer.Option(None, envvar="WB_TOKEN_WAREHOUSE", help="API token"),
    json_output: bool = typer.Option(False, "--json", help="Output in JSON format"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose logging")
):
    """Get list of all seller warehouses."""
    if not token:
        token = settings.token_warehouse
    if not token:
        console.print("[red]Error: API token not provided.[/red]")
        raise typer.Exit(code=1)

    try:
        client = SyncClient(token=token)
        service = WarehouseService(client)
        
        if verbose:
            console.print("Fetching warehouses...")
            
        warehouses = service.get_warehouses()

        if json_output:
            console.print([w.model_dump_json() for w in warehouses])
        else:
            table = Table(title="Seller Warehouses")
            table.add_column("ID", style="cyan")
            table.add_column("Name", style="magenta")
            table.add_column("Office ID", style="green")

            for w in warehouses:
                table.add_row(str(w.id), w.name, str(w.office_id))
            
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
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(code=1)
