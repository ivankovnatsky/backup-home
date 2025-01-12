import os
import time
import logging
import subprocess
from pathlib import Path
from backup_home.platform import get_excludes

logger = logging.getLogger("backup-home")

def create_backup(source_dir: str, verbose: bool = False) -> str:
    """Create a backup archive using 7-Zip."""
    current_user = os.getenv("USERNAME")
    backup_file = f"C:\\Windows\\Temp\\{current_user}.zip"

    try:
        logger.info(f"Creating backup of directory: {source_dir}")

        # Check if 7z is available
        if not subprocess.run(["where", "7z"], capture_output=True).returncode == 0:
            raise Exception("7z is not found in PATH. Please install 7-Zip first.")

        # Build 7z command with excludes
        args = [
            "7z",
            "a",  # Add to archive
            "-tzip",  # ZIP format
            "-mx=0",  # Store only, no compression
            "-r",  # Recursive
            "-y",  # Yes to all queries
            "-ssw",  # Compress files open for writing
            backup_file,  # Output file
            os.path.join(source_dir, "*"),  # Source directory
        ]

        # Add exclude patterns
        for exclude in get_excludes():
            args.append(f"-xr!{exclude}")

        # Run 7z command
        process = subprocess.run(args, capture_output=True, text=True)

        # Handle exit codes
        if process.returncode not in [0, 1, 2]:
            raise Exception(f"7-Zip failed with exit code {process.returncode}")

        if process.returncode == 0:
            logger.info("Archive created successfully with no warnings.")
        elif process.returncode == 1:
            logger.info("Archive created successfully with some files skipped.")
        else:  # returncode == 2
            logger.info(
                "Archive created with some files skipped (locked files or permissions)."
            )

        # Verify the archive was created
        if os.path.exists(backup_file):
            backup_size = os.path.getsize(backup_file) / (
                1024 * 1024 * 1024
            )  # Size in GB
            logger.info("Backup completed successfully!")
            logger.info(f"Backup archive size: {backup_size:.2f} GB")
            return backup_file
        else:
            raise Exception("Failed to create backup archive")

    except Exception as e:
        logger.error(f"Error during backup: {str(e)}")
        raise
