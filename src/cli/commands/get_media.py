import typer
from rich.console import Console
from src.config import settings
from wildberries_python_sdk.client_sync import SyncClient
from src.services.media import MediaService
from wildberries_python_sdk.exceptions.base import TooManyRequestsError

app = typer.Typer()
console = Console()

@app.command()
def get_media(
    nm_id: int = typer.Option(..., help="NM ID"),
    token: str = typer.Option(None, envvar="WB_TOKEN_MEDIA", help="API token"),
    json_output: bool = typer.Option(False, "--json", help="Output in JSON format"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose logging")
):
    """Get media for a product."""
    if not token:
        token = settings.token_media
    if not token:
        console.print("[red]Error: API token not provided.[/red]")
        raise typer.Exit(code=1)

    try:
        client = SyncClient(token=token)
        service = MediaService(client)
        
        if verbose:
            console.print(f"Fetching media for NM ID {nm_id}...")
            
        media = service.get_media(nm_id=nm_id)

        if json_output:
            console.print(media.model_dump_json())
        else:
            console.print(f"NM ID: {media.nm_id}")
            console.print(f"Photo Links: {', '.join(media.photo_links)}")
            
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
