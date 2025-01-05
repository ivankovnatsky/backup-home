#!/usr/bin/env python3

import os
import sys
import argparse
from datetime import datetime
from pathlib import Path

from backup_home.backup import create_backup
from backup_home.upload import upload_to_rclone


def log(message: str) -> None:
    """Print a message with a timestamp prefix."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")


def main():
    examples = """
Examples:
    backup-home drive:
    backup-home gdrive:backup/home
    backup-home remote:path/to/backup/dir"""

    parser = argparse.ArgumentParser(
        description="Backup home directory and upload to rclone destination",
        epilog=examples,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "destination",
        help='Rclone destination path (e.g., "drive:", "gdrive:backup/home")',
    )
    parser.add_argument(
        "--source",
        "-s",
        help="Source directory to backup (defaults to home directory)",
        default=str(Path.home()),
    )
    parser.add_argument(
        "--preview",
        action="store_true",
        help="Preview what would be done without actually doing it",
    )

    # Show help if no arguments are provided
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    # Check if the destination includes a cloud name
    if ":" not in args.destination:
        log("Error: Destination must include a cloud name (e.g., 'drive:').")
        sys.exit(1)

    if args.preview:
        log("\nPreview summary:")
        log("---------------")
        log(f"Source: {args.source}")
        log(f"Destination: {args.destination}")
        log("\nThis would:")
        log(f"1. Create backup archive of: {args.source}")
        log(f"2. Upload to: {args.destination}")
        log("3. Clean up temporary files")
        sys.exit(0)

    try:
        backup_path = create_backup(args.source)
        if backup_path:
            try:
                upload_to_rclone(backup_path, args.destination)
            finally:
                if os.path.exists(backup_path):
                    os.remove(backup_path)
    except Exception as e:
        log(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
