# backup-home

A Python utility to backup home directory to cloud storage using rclone.

## Features

- Cross-platform support (macOS and Windows)
- Efficient compression (pigz on macOS, 7-Zip on Windows)
- Smart file exclusion patterns
- Cloud storage upload via rclone
- Progress reporting

## Requirements

- Python 3.8 or later
- rclone (configured with your cloud storage)
- On macOS: pigz
- On Windows: 7-Zip

## Installation

### Using Nix Flakes

Enable flakes in your nix configuration

```console
nix develop # For development environment

or

```console
nix profile install
```

```console
poetry install
```

Show help

```console
backup-home --help
```

Backup home directory to Google Drive

```console
backup-home drive:backup/home
```

Backup specific directory

```console
backup-home -s /path/to/directory drive:backup/custom
```

Preview what would be backed up

```console
backup-home --preview drive:backup/home
```
