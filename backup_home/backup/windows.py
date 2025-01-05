import os
import subprocess
from datetime import datetime
from backup_home.platform import get_excludes


def log(message: str) -> None:
    """Print a message with a timestamp prefix."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")


def create_backup(source_dir: str) -> str:
    """Create a ZIP backup of the specified directory using 7-Zip."""
    backup_file = os.path.join(
        os.environ.get("TEMP", "C:\\Windows\\Temp"), f"{os.environ['USERNAME']}.zip"
    )

    try:
        log(f"Creating backup of directory: {source_dir}")

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
            log("Archive created successfully with no warnings.")
        elif process.returncode == 1:
            log("Archive created successfully with some files skipped.")
        else:  # returncode == 2
            log(
                "Archive created with some files skipped (locked files or permissions)."
            )

        # Verify the archive was created
        if os.path.exists(backup_file):
            backup_size = os.path.getsize(backup_file) / (
                1024 * 1024 * 1024
            )  # Size in GB
            log(f"Backup completed successfully!")
            log(f"Backup archive size: {backup_size:.2f} GB")
            return backup_file
        else:
            raise Exception("Failed to create backup archive")

    except Exception as e:
        log(f"ERROR: {str(e)}")
        raise
