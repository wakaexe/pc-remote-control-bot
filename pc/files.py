"""
File management module
Handles file operations: list, download, upload, create, delete
"""
import os
from pathlib import Path
from typing import List, Dict, Tuple
from datetime import datetime
import config
from utils.logger import logger
from utils.helpers import format_bytes, get_file_icon, is_safe_to_delete, sanitize_path

def list_directory(path: str = None) -> Tuple[str, List[Dict]]:
    """
    List files and directories at given path

    Args:
        path: Directory path (defaults to user home)

    Returns:
        Tuple of (formatted string, list of items for navigation)
    """
    try:
        if path is None:
            path = str(Path.home())

        target_path = Path(path).resolve()

        if not target_path.exists():
            return f"❌ Path does not exist: {path}", []

        if not target_path.is_dir():
            return f"❌ Not a directory: {path}", []

        items = []
        result_lines = [f"📁 **{target_path}**\n"]

        # Add parent directory option
        if target_path.parent != target_path:
            items.append({
                'name': '..',
                'path': str(target_path.parent),
                'is_dir': True,
                'size': 0
            })

        # List all items
        try:
            for item in sorted(target_path.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower())):
                try:
                    stat = item.stat()
                    is_dir = item.is_dir()
                    size = 0 if is_dir else stat.st_size
                    modified = datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M')

                    icon = '📁' if is_dir else get_file_icon(item.name)
                    size_str = '<DIR>' if is_dir else format_bytes(size)

                    result_lines.append(f"{icon} {item.name:<40} {size_str:>10} {modified}")

                    items.append({
                        'name': item.name,
                        'path': str(item),
                        'is_dir': is_dir,
                        'size': size
                    })

                except (PermissionError, OSError):
                    result_lines.append(f"⚠️ {item.name} (access denied)")

        except PermissionError:
            return f"❌ Permission denied: {path}", []

        if len(items) <= 1:  # Only parent dir
            result_lines.append("\n(Empty directory)")

        return "\n".join(result_lines), items

    except Exception as e:
        logger.error(f"Failed to list directory {path}: {e}")
        return f"❌ Error: {str(e)}", []

def download_file(file_path: str) -> Tuple[bool, str, Path]:
    """
    Prepare file for download

    Args:
        file_path: Path to file

    Returns:
        Tuple of (success, message, file_path)
    """
    try:
        target_path = Path(file_path).resolve()

        if not target_path.exists():
            return False, f"❌ File does not exist: {file_path}", None

        if not target_path.is_file():
            return False, f"❌ Not a file: {file_path}", None

        file_size = target_path.stat().st_size

        if file_size > config.MAX_FILE_SIZE:
            return False, f"❌ File too large: {format_bytes(file_size)} (max {format_bytes(config.MAX_FILE_SIZE)})", None

        logger.info(f"Preparing file for download: {target_path}")
        return True, f"📤 Sending file: {target_path.name} ({format_bytes(file_size)})", target_path

    except Exception as e:
        logger.error(f"Failed to prepare file for download {file_path}: {e}")
        return False, f"❌ Error: {str(e)}", None

def upload_file(file_path: Path, destination: str = None) -> str:
    """
    Handle uploaded file

    Args:
        file_path: Path to downloaded file
        destination: Destination directory (defaults to Downloads)

    Returns:
        Status message
    """
    try:
        if destination is None:
            destination = str(Path.home() / "Downloads")

        dest_dir = Path(destination).resolve()
        dest_dir.mkdir(parents=True, exist_ok=True)

        dest_file = dest_dir / file_path.name

        # Handle duplicate names
        counter = 1
        while dest_file.exists():
            stem = file_path.stem
            suffix = file_path.suffix
            dest_file = dest_dir / f"{stem}_{counter}{suffix}"
            counter += 1

        # Move file
        file_path.rename(dest_file)

        logger.info(f"File uploaded to: {dest_file}")
        return f"✅ File saved to: {dest_file}"

    except Exception as e:
        logger.error(f"Failed to upload file: {e}")
        return f"❌ Error: {str(e)}"

def create_directory(path: str) -> str:
    """
    Create new directory

    Args:
        path: Directory path to create

    Returns:
        Status message
    """
    try:
        target_path = Path(path).resolve()

        if target_path.exists():
            return f"⚠️ Path already exists: {path}"

        target_path.mkdir(parents=True, exist_ok=True)

        logger.info(f"Directory created: {target_path}")
        return f"✅ Directory created: {target_path}"

    except Exception as e:
        logger.error(f"Failed to create directory {path}: {e}")
        return f"❌ Error: {str(e)}"

def delete_path(path: str) -> str:
    """
    Delete file or empty directory

    Args:
        path: Path to delete

    Returns:
        Status message
    """
    try:
        target_path = Path(path).resolve()

        if not target_path.exists():
            return f"❌ Path does not exist: {path}"

        # Safety check
        if not is_safe_to_delete(target_path):
            return f"⛔ Cannot delete system path: {path}"

        if target_path.is_file():
            target_path.unlink()
            logger.info(f"File deleted: {target_path}")
            return f"✅ File deleted: {target_path}"
        elif target_path.is_dir():
            if any(target_path.iterdir()):
                return f"❌ Directory not empty: {path}"
            target_path.rmdir()
            logger.info(f"Directory deleted: {target_path}")
            return f"✅ Directory deleted: {target_path}"
        else:
            return f"❌ Unknown path type: {path}"

    except Exception as e:
        logger.error(f"Failed to delete {path}: {e}")
        return f"❌ Error: {str(e)}"

def get_directory_tree(path: str = None, max_depth: int = 3, current_depth: int = 0) -> str:
    """
    Get directory tree structure

    Args:
        path: Root directory path
        max_depth: Maximum depth to traverse
        current_depth: Current recursion depth

    Returns:
        Formatted tree string
    """
    try:
        if path is None:
            path = str(Path.home())

        target_path = Path(path).resolve()

        if not target_path.exists() or not target_path.is_dir():
            return f"❌ Invalid directory: {path}"

        lines = []
        if current_depth == 0:
            lines.append(f"📁 {target_path}\n")

        if current_depth >= max_depth:
            return "\n".join(lines)

        try:
            items = sorted(target_path.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower()))

            for i, item in enumerate(items[:50]):  # Limit to 50 items per level
                is_last = i == len(items) - 1
                prefix = "└── " if is_last else "├── "
                indent = "    " * current_depth

                try:
                    if item.is_dir():
                        lines.append(f"{indent}{prefix}📁 {item.name}/")
                        if current_depth < max_depth - 1:
                            subtree = get_directory_tree(str(item), max_depth, current_depth + 1)
                            if subtree:
                                lines.append(subtree)
                    else:
                        size = format_bytes(item.stat().st_size)
                        icon = get_file_icon(item.name)
                        lines.append(f"{indent}{prefix}{icon} {item.name} ({size})")

                except (PermissionError, OSError):
                    lines.append(f"{indent}{prefix}⚠️ {item.name} (access denied)")

            if len(items) > 50:
                lines.append(f"{indent}... and {len(items) - 50} more items")

        except PermissionError:
            lines.append(f"{'    ' * current_depth}⚠️ (access denied)")

        return "\n".join(lines)

    except Exception as e:
        logger.error(f"Failed to generate tree for {path}: {e}")
        return f"❌ Error: {str(e)}"
