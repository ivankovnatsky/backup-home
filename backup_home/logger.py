import logging
from rich.logging import RichHandler
from rich.console import Console

console = Console()

def setup_logger(verbose: bool = False) -> logging.Logger:
    """Configure and return the application logger."""
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(
            console=console,
            rich_tracebacks=True,
            markup=True,
            show_time=True
        )]
    )
    return logging.getLogger("backup-home") 
