import typer
from rich.console import Console
from rich.table import Table
from typing import List
from src.config import settings
from wildberries_python_sdk.client_sync import SyncClient
from src.services.inventory import InventoryService
from wildberries_python_sdk.exceptions.base import TooManyRequestsError

app = typer.Typer()
console = Console()

@app.command()
def get_inventory(
    warehouse_id: int = typer.Option(..., help="Warehouse ID"),
    chrt_ids: List[int] = typer.Option(..., help="List of chrt IDs"),
    token: str = typer.Option(None, envvar="WB_TOKEN_INVENTORY", help="API token"),
    json_output: bool = typer.Option(False, "--json", help="Output in JSON format"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose logging")
):
    """Get product inventory for a specific warehouse."""
    if not token:
        token = settings.token_inventory
    if not token:
        console.print("[red]Error: API token not provided.[/red]")
        raise typer.Exit(code=1)

    try:
        client = SyncClient(token=token)
        service = InventoryService(client)
        
        if verbose:
            console.print(f"Fetching inventory for warehouse {warehouse_id}...")
            
        items = service.get_inventory(warehouse_id=warehouse_id, chrt_ids=chrt_ids)

        if json_output:
            console.print([i.model_dump_json() for i in items])
        else:
            table = Table(title=f"Inventory for Warehouse {warehouse_id}")
            table.add_column("Chrt ID", style="cyan")
            table.add_column("Amount", style="magenta")

            for item in items:
                table.add_row(str(item.chrt_id), str(item.amount))
            
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
