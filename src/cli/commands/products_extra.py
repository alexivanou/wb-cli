import typer
from rich.console import Console
from rich.table import Table
from src.config import settings
from wildberries_python_sdk.client_sync import SyncClient
from src.services.products_extra import ProductsServiceExtra
from wildberries_python_sdk.exceptions.base import TooManyRequestsError

products_app = typer.Typer()
console = Console()

@products_app.command(name="get-brands")
def get_brands(
    token: str = typer.Option(None, envvar="WB_TOKEN_PRODUCTS", help="API token"),
    json_output: bool = typer.Option(False, "--json", help="Output in JSON format"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose logging")
):
    """Get list of brands."""
    if not token:
        token = settings.token_products
    if not token:
        console.print("[red]Error: API token not provided.[/red]")
        raise typer.Exit(code=1)
    try:
        client = SyncClient(token=token)
        service = ProductsServiceExtra(client)
        data = service.get_brands()
        if json_output:
            console.print(str(data))
        else:
            table = Table(title="Brands")
            table.add_column("ID", style="cyan")
            table.add_column("Name", style="magenta")
            for d in data:
                table.add_row(str(d.get("id", "")), d.get("name", ""))
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

@products_app.command(name="get-subjects")
def get_subjects(
    token: str = typer.Option(None, envvar="WB_TOKEN_PRODUCTS", help="API token"),
    json_output: bool = typer.Option(False, "--json", help="Output in JSON format"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose logging")
):
    """Get list of subjects."""
    if not token:
        token = settings.token_products
    if not token:
        console.print("[red]Error: API token not provided.[/red]")
        raise typer.Exit(code=1)
    try:
        client = SyncClient(token=token)
        service = ProductsServiceExtra(client)
        data = service.get_subjects()
        if json_output:
            console.print(str(data))
        else:
            table = Table(title="Subjects")
            table.add_column("ID", style="cyan")
            table.add_column("Name", style="magenta")
            for d in data:
                table.add_row(str(d.get("id", "")), d.get("name", ""))
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