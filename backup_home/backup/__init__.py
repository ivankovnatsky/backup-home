import sys
from datetime import datetime
from . import macos, windows


def log(message: str) -> None:
    """Print a message with a timestamp prefix."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")


def create_backup(source_dir: str) -> str:
    """Create backup archive of the specified directory."""
    if sys.platform == "darwin":
        return macos.create_backup(source_dir)
    elif sys.platform == "win32":
        return windows.create_backup(source_dir)
    else:
        raise NotImplementedError(f"Platform {sys.platform} is not supported")
