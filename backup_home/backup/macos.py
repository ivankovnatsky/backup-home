import os
import subprocess
import errno
from datetime import datetime
from backup_home.platform import get_excludes


def log(message: str) -> None:
    """Print a message with a timestamp prefix."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")


def create_backup(source_dir: str) -> str:
    """Create a tar.gz backup of the specified directory."""
    current_user = os.getenv("USER")
    backup_file = f"/tmp/{current_user}.tar.gz"

    try:
        log(f"Creating backup of directory: {source_dir}")

        # Get parent directory and base name
        parent_dir = os.path.dirname(source_dir)
        base_name = os.path.basename(source_dir)

        # Build tar command
        tar_cmd = ["/usr/bin/tar"]
        tar_cmd.extend(["-cvf", "-"])

        # Add exclude patterns
        for exclude in get_excludes():
            tar_cmd.extend(["--exclude", f"{exclude}"])

        # Add source last (just the username since we're in /Users)
        tar_cmd.append(base_name)

        log(
            f"Running command from {parent_dir}: {' '.join(tar_cmd)} | pigz > {backup_file}"
        )

        # Create backup using tar and pigz
        with open(backup_file, "wb") as f:
            tar_proc = subprocess.Popen(
                tar_cmd,
                stdout=subprocess.PIPE,
                cwd=parent_dir,  # Run from /Users directory
            )
            pigz_proc = subprocess.Popen(["pigz"], stdin=tar_proc.stdout, stdout=f)
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
            backup_size = os.path.getsize(backup_file) / (
                1024 * 1024 * 1024
            )  # Size in GB
            log(f"Backup completed successfully!")
            log(f"Backup archive size: {backup_size:.2f} GB")
            return backup_file
        else:
            raise Exception("Failed to create backup archive")

    except subprocess.TimeoutExpired:
        log("Backup process timed out")
        raise
    except OSError as e:
        if e.errno == errno.EINTR:  # Interrupted system call
            log("Backup was interrupted, retrying...")
            return create_backup(source_dir)  # Recursive retry
        raise
