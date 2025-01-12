import os
import time
import logging
from rclone_python import rclone
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    BarColumn,
    TaskProgressColumn,
    TransferSpeedColumn,
    TimeRemainingColumn,
)

logger = logging.getLogger("backup-home")

def upload_to_rclone(source: str, destination: str) -> None:
    """Upload file to rclone destination."""
    logger.info("\nStarting upload...")

    try:
        start_time = time.time()

        # Create custom progress bar with matching format
        pbar = Progress(
            SpinnerColumn(),
            TextColumn("[cyan]Uploading to cloud[/cyan]"),
            BarColumn(),
            TextColumn("{task.percentage:>3.0f}%"),
            TransferSpeedColumn(),
            TimeRemainingColumn(),
            refresh_per_second=1/2,
            transient=False
        )

        # Upload using rclone
        rclone.copy(source, destination, pbar=pbar)

        # Calculate and log statistics
        elapsed = time.time() - start_time
        file_size_mb = os.path.getsize(source) / (1024 * 1024)
        mb_per_sec = file_size_mb / elapsed

        logger.info(f"\nUpload completed: {file_size_mb:.2f} MB transferred ({mb_per_sec:.2f} MB/s)")

    except Exception as e:
        raise Exception(f"rclone upload failed: {str(e)}")
