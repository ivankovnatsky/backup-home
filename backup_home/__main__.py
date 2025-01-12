#!/usr/bin/env python3

import os
import sys
import shutil
from pathlib import Path
import click
from rich.console import Console

from backup_home.backup import create_backup
from backup_home.upload import upload_to_rclone
from backup_home.logger import setup_logger

console = Console()

def check_dependencies():
    """Verify that all required system dependencies are available."""
    missing = []
    
    # Check rclone (required for all platforms)
    if not shutil.which('rclone'):
        missing.append('rclone')
    
    # Check platform-specific dependencies
    if sys.platform == "darwin":
        if not shutil.which('pigz'):
            missing.append('pigz')
    elif sys.platform == "win32":
        if not shutil.which('7z'):
            missing.append('7-Zip')
    elif sys.platform.startswith('linux'):
        if not shutil.which('tar'):
            missing.append('tar')
        if not shutil.which('gzip'):
            missing.append('gzip')
            
    if missing:
        console.print(f"[red]Error: Missing required dependencies: {', '.join(missing)}[/red]")
        console.print("\nPlease install them using one of the following methods:")
        console.print("1. Using nix: nix profile install")
        console.print("2. Using your system package manager")
        sys.exit(1)

@click.command()
@click.argument('destination')
@click.option('--source', '-s', 
    default=str(Path.home()),
    help='Source directory to backup (defaults to home directory)'
)
@click.option('--preview', is_flag=True,
    help='Preview what would be done without actually doing it'
)
@click.option('--verbose', '-v', is_flag=True,
    help='Show verbose output'
)
def main(destination: str, source: str, preview: bool, verbose: bool):
    """Backup home directory to cloud storage using rclone."""
    # Check dependencies first
    check_dependencies()
    
    # Set up logging
    logger = setup_logger(verbose)
    
    try:
        # Check if the destination includes a cloud name
        if ":" not in destination:
            logger.error("Destination must include a cloud name (e.g., 'drive:').")
            sys.exit(1)

        if preview:
            console.print("\n[bold]Preview summary:[/bold]")
            console.print("---------------")
            console.print(f"Source: {source}")
            console.print(f"Destination: {destination}")
            console.print("\nThis would:")
            console.print(f"1. Create backup archive of: {source}")
            console.print(f"2. Upload to: {destination}")
            console.print("3. Clean up temporary files")
            return

        # Create backup - removed the console.status wrapper
        backup_path = create_backup(source, verbose)
        
        # Upload to destination
        upload_to_rclone(backup_path, destination)
        
        # Clean up
        os.unlink(backup_path)
        logger.info("Temporary files cleaned up")
        logger.info("Backup completed successfully!")

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
