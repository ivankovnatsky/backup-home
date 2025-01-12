import os
import time
import logging
import subprocess
from pathlib import Path
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.live import Live
from backup_home.platform import get_excludes

logger = logging.getLogger("backup-home")

def create_backup(source_dir: str, verbose: bool = False) -> str:
    """Create a tar.gz backup using tar and pigz."""
    current_user = os.getenv("USER")
    backup_file = f"/tmp/{current_user}.tar.gz"

    try:
        # Get exclude patterns first, silently
        exclude_patterns = get_excludes()

        # Create progress display immediately
        progress = Progress(
            SpinnerColumn(),
            TextColumn("[cyan]Creating archive[/cyan]"),
            BarColumn(),
            TextColumn("{task.percentage:>3.0f}%"),
            TextColumn("({task.fields[speed]} MB/s)"),
            TextColumn("{task.fields[size]} MB"),
            TimeElapsedColumn(),
            refresh_per_second=1/2,
            transient=False
        )

        # Build tar command with excludes
        tar_cmd = ["/usr/bin/tar"]
        if verbose:
            tar_cmd.append("-cvf")
        else:
            tar_cmd.append("-cf")
        tar_cmd.append("-")
        for pattern in exclude_patterns:
            tar_cmd.extend(["--exclude", pattern])
        tar_cmd.append(".")

        with Live(progress, refresh_per_second=1/2):
            task = progress.add_task(
                "",
                total=None,
                speed="0.0",
                size="0.0"
            )
            
            start_time = time.time()
            with open(backup_file, "wb") as f:
                tar_proc = subprocess.Popen(
                    tar_cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE if verbose else subprocess.DEVNULL,
                    cwd=source_dir
                )
                pigz_proc = subprocess.Popen(
                    ["pigz", "-p", str(os.cpu_count())],
                    stdin=tar_proc.stdout,
                    stdout=f,
                    stderr=subprocess.PIPE
                )
                tar_proc.stdout.close()

                # Monitor progress with 2-second interval
                last_update = time.time()
                update_interval = 2.0  # Update every 2 seconds
                
                while tar_proc.poll() is None or pigz_proc.poll() is None:
                    current_time = time.time()
                    if current_time - last_update >= update_interval:
                        if os.path.exists(backup_file):
                            current_size = os.path.getsize(backup_file)
                            elapsed = time.time() - start_time
                            speed = current_size / (1024 * 1024 * elapsed)  # MB/s
                            
                            progress.update(
                                task,
                                speed=f"{speed:.1f}",
                                size=f"{current_size / (1024*1024):.1f}"
                            )
                            last_update = current_time
                    time.sleep(0.1)

                # Check results
                if pigz_proc.wait() != 0:
                    raise Exception("Compression failed")
                if tar_proc.wait() != 0:
                    raise Exception("Tar process failed")

        # Final statistics
        if os.path.exists(backup_file):
            elapsed = time.time() - start_time
            backup_size_mb = os.path.getsize(backup_file) / (1024 * 1024)
            mb_per_sec = backup_size_mb / elapsed

            logger.info("Backup completed successfully!")
            logger.info(f"Final archive size: {backup_size_mb:.2f} MB (average speed: {mb_per_sec:.2f} MB/s)")
            return backup_file
        else:
            raise Exception("Failed to create backup archive")

    except Exception as e:
        logger.error(f"Error during backup: {str(e)}")
        raise
