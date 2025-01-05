import os
import subprocess
from datetime import datetime


def log(message: str) -> None:
    """Print a message with a timestamp prefix."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")


def upload_to_rclone(source: str, destination: str) -> None:
    """Upload file to rclone destination."""
    log(f"Uploading backup to {destination}...")

    try:
        # Check if rclone is available
        if (
            subprocess.run(
                ["which" if os.name != "nt" else "where", "rclone"], capture_output=True
            ).returncode
            != 0
        ):
            raise Exception("rclone is not found in PATH. Please install rclone first.")

        # Upload using rclone
        subprocess.run(
            ["rclone", "copy", "--progress", source, destination], check=True
        )

        log("Upload completed successfully!")

    except subprocess.CalledProcessError as e:
        raise Exception(f"rclone upload failed with exit code {e.returncode}")
