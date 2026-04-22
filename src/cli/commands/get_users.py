import typer
from rich.console import Console
from rich.table import Table
from src.config import settings
from wildberries_python_sdk.client_sync import SyncClient
from src.services.general import GeneralService
from wildberries_python_sdk.exceptions.base import TooManyRequestsError

app = typer.Typer()
console = Console()

@app.command(name="get-users")
def get_users(
    limit: int = typer.Option(100, help="Number of users to return"),
    offset: int = typer.Option(0, help="Offset for pagination"),
    is_invite_only: bool = typer.Option(False, help="Show only invited users"),
    token: str = typer.Option(None, envvar="WB_TOKEN_GENERAL", help="API token"),
    json_output: bool = typer.Option(False, "--json", help="Output in JSON format"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose logging")
):
    """Get list of users."""
    if not token:
        token = settings.token_general
    if not token:
        console.print("[red]Error: API token not provided.[/red]")
        raise typer.Exit(code=1)

    try:
        client = SyncClient(token=token)
        service = GeneralService(client)
        
        if verbose:
            console.print(f"Fetching users...")
            
        users = service.get_users(limit=limit, offset=offset, is_invite_only=is_invite_only)

        if json_output:
            console.print([u.model_dump_json() for u in users])
        else:
            table = Table(title="Users")
            table.add_column("ID", style="cyan")
            table.add_column("Name", style="magenta")
            table.add_column("Role", style="green")
            for u in users:
                table.add_row(str(u.id), u.name, u.role)
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