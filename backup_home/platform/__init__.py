import sys
from . import macos, windows


def get_excludes():
    """Get platform-specific exclude patterns."""
    if sys.platform == "darwin":
        return macos.get_excludes()
    elif sys.platform == "win32":
        return windows.get_excludes()
    else:
        return []
