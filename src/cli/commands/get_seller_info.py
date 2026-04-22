import typer
from rich.console import Console
from src.config import settings
from wildberries_python_sdk.client_sync import SyncClient
from src.services.general import GeneralService
from wildberries_python_sdk.exceptions.base import TooManyRequestsError

app = typer.Typer()
console = Console()

@app.command()
def get_seller_info(
    token: str = typer.Option(None, envvar="WB_TOKEN_GENERAL", help="API token"),
    json_output: bool = typer.Option(False, "--json", help="Output in JSON format"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose logging")
):
    """Get seller information."""
    if not token:
        token = settings.token_general
    if not token:
        console.print("[red]Error: API token not provided.[/red]")
        raise typer.Exit(code=1)

    try:
        client = SyncClient(token=token)
        service = GeneralService(client)
        
        if verbose:
            console.print("Fetching seller info...")
            
        seller_info = service.get_seller_info()

        if json_output:
            console.print(seller_info.model_dump_json())
        else:
            console.print(f"Seller Name: {seller_info.name}")
            console.print(f"Supplier ID: {seller_info.supplier_id}")
            
    except TooManyRequestsError as e:
        if verbose:
            console.print(f"[debug] Exception details: {e}")
            console.print(f"[debug] Retry-After value: {e.retry_after}")
            if e.raw_response:
                console.print(f"[debug] Raw response: {e.raw_response}")
            if e.response_headers:
                console.print(f"[debug] Response headers: {e.response_headers}")
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
            if hasattr(e, 'response_headers') and e.response_headers:
                console.print(f"[debug] Response headers: {e.response_headers}")
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(code=1)
