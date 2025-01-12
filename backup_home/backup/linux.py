import os
import time
import logging
import subprocess
from pathlib import Path
from backup_home.platform import get_excludes

logger = logging.getLogger("backup-home")

def create_backup(source_dir: str, verbose: bool = False) -> str:
    """Create a tar.gz backup of the specified directory."""
    current_user = os.getenv("USER")
    backup_file = f"/tmp/{current_user}.tar.gz"

    try:
        logger.info(f"Creating backup of directory: {source_dir}")

        # Get parent directory and base name
        parent_dir = os.path.dirname(source_dir)
        base_name = os.path.basename(source_dir)

        # Build tar command
        tar_cmd = ["/usr/bin/tar"]
        tar_cmd.extend([
            "-cvf",
            "-"
        ])
        
        # Add exclude patterns
        for exclude in get_excludes():
            tar_cmd.extend(["--exclude", exclude])
            
        # Add source last
        tar_cmd.append(base_name)

        logger.info(f"Running command from {parent_dir}: {' '.join(tar_cmd)} | pigz > {backup_file}")
        
        # Create backup using tar and pigz
        with open(backup_file, "wb") as f:
            tar_proc = subprocess.Popen(
                tar_cmd,
                stdout=subprocess.PIPE,
                cwd=parent_dir
            )
            pigz_proc = subprocess.Popen(
                ["pigz"],
                stdin=tar_proc.stdout,
                stdout=f
            )
            tar_proc.stdout.close()  # Allow tar to receive SIGPIPE

            # Add timeout and better error handling
            ret_code = pigz_proc.wait(timeout=3600)  # 1 hour timeout
            if ret_code != 0:
                raise Exception(f"Compression failed with code {ret_code}")

            # Check tar process result too
            if tar_proc.wait() != 0:
                raise Exception("Tar process failed")

        # Verify the archive was created
        if os.path.exists(backup_file):
            backup_size = os.path.getsize(backup_file) / (1024 * 1024 * 1024)  # Size in GB
            logger.info("Backup completed successfully!")
            logger.info(f"Backup archive size: {backup_size:.2f} GB")
            return backup_file
        else:
            raise Exception("Failed to create backup archive")

    except subprocess.TimeoutExpired:
        logger.error("Backup process timed out")
        raise
    except OSError as e:
        if e.errno == errno.EINTR:  # Interrupted system call
            logger.info("Backup was interrupted, retrying...")
            return create_backup(source_dir)  # Recursive retry
        raise 
