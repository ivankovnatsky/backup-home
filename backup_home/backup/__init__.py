import sys
import logging
from . import macos, windows, linux

logger = logging.getLogger("backup-home")

def create_backup(source_dir: str, verbose: bool = False) -> str:
    """Create backup archive of the specified directory."""
    if sys.platform == "darwin":
        return macos.create_backup(source_dir, verbose)
    elif sys.platform == "win32":
        return windows.create_backup(source_dir, verbose)
    elif sys.platform.startswith("linux"):
        return linux.create_backup(source_dir, verbose)
    else:
        raise NotImplementedError(f"Platform {sys.platform} is not supported")

def get_excludes():
    """Get platform-specific exclude patterns."""
    if sys.platform == "darwin":
        return macos.get_excludes()
    elif sys.platform == "win32":
        return windows.get_excludes()
    elif sys.platform.startswith("linux"):
        return linux.get_excludes()
    else:
        return []
