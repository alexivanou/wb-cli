import typer
from rich.console import Console
from src.config import settings
from wildberries_python_sdk.client_sync import SyncClient
from src.services.general import GeneralService
from wildberries_python_sdk.exceptions.base import TooManyRequestsError

app = typer.Typer()
console = Console()

@app.command(name="get-news")
def get_news(
    from_date: str = typer.Option(None, help="Filter news from date (YYYY-MM-DD)"),
    from_id: int = typer.Option(None, help="Filter news from ID"),
    token: str = typer.Option(None, envvar="WB_TOKEN_GENERAL", help="API token"),
    json_output: bool = typer.Option(False, "--json", help="Output in JSON format"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose logging")
):
    """Get news from portal."""
    if not token:
        token = settings.token_general
    if not token:
        console.print("[red]Error: API token not provided.[/red]")
        raise typer.Exit(code=1)

    try:
        client = SyncClient(token=token)
        service = GeneralService(client)
        
        if verbose:
            console.print("Fetching news...")
            
        news = service.get_news(from_date=from_date, from_id=from_id)

        if json_output:
            console.print([n.model_dump_json() for n in news])
        else:
            for n in news:
                console.print(f"[{n.id}] {n.title}")
            
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

@app.command(name="get-rating")
def get_rating(
    token: str = typer.Option(None, envvar="WB_TOKEN_GENERAL", help="API token"),
    json_output: bool = typer.Option(False, "--json", help="Output in JSON format"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose logging")
):
    """Get seller rating."""
    if not token:
        token = settings.token_general
    if not token:
        console.print("[red]Error: API token not provided.[/red]")
        raise typer.Exit(code=1)

    try:
        client = SyncClient(token=token)
        service = GeneralService(client)
        
        if verbose:
            console.print("Fetching rating...")
            
        rating = service.get_rating()

        if json_output:
            console.print(rating.model_dump_json())
        else:
            console.print(f"Supplier ID: {rating.supplier_id}")
            console.print(f"Rating: {rating.rating}")
            
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

@app.command(name="ping")
def ping(
    server_key: str = typer.Option("common", help="Server key"),
    token: str = typer.Option(None, envvar="WB_TOKEN_GENERAL", help="API token"),
    json_output: bool = typer.Option(False, "--json", help="Output in JSON format"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose logging")
):
    """Check connection to API."""
    if not token:
        token = settings.token_general
    if not token:
        console.print("[red]Error: API token not provided.[/red]")
        raise typer.Exit(code=1)

    try:
        client = SyncClient(token=token)
        service = GeneralService(client)
        
        if verbose:
            console.print(f"Pinging {server_key}...")
            
        result = service.ping()

        if json_output:
            console.print(str(result))
        else:
            console.print("[green]Connection OK![/green]")
            console.print(f"Server time: {result}")
            
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