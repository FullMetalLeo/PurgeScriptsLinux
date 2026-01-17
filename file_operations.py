#!/usr/bin/env python3
"""
File Operations Script - Cut, Copy, Paste
==========================================
Cross-platform file operation script that replicates Windows cut, copy, and paste functionality.
Supports Windows, Linux, Unix, and macOS.

Features:
- Cut files/folders (move operation)
- Copy files/folders
- Paste to destination
- Conflict resolution (replace, keep both, skip)
- Comprehensive exception handling
- Cross-platform compatibility

Author: Auto-generated
Date: 2026-01-17
"""

import os
import shutil
import sys
from pathlib import Path
from typing import List, Optional, Tuple
from enum import Enum


class OperationType(Enum):
    """Enumeration for operation types"""
    COPY = "copy"
    CUT = "cut"


class ConflictAction(Enum):
    """Enumeration for file conflict resolution actions"""
    REPLACE = "replace"
    KEEP_BOTH = "keep_both"
    SKIP = "skip"


class FileOperationError(Exception):
    """Custom exception for file operation errors"""
    pass


class FileOperations:
    """
    Main class for handling file cut, copy, and paste operations.
    """
    
    def __init__(self):
        """Initialize the FileOperations class"""
        self.clipboard = []  # List to store file paths
        self.operation_type = None  # Type of operation (cut or copy)
        
    def copy(self, paths: List[str]) -> bool:
        """
        Copy files or directories to clipboard.
        
        Args:
            paths (List[str]): List of file/directory paths to copy
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Validate all paths exist before copying
            validated_paths = []
            for path_str in paths:
                path = Path(path_str)
                if not path.exists():
                    print(f"❌ Error: Path does not exist: {path_str}")
                    return False
                validated_paths.append(path.absolute())
            
            # Store paths in clipboard
            self.clipboard = validated_paths
            self.operation_type = OperationType.COPY
            
            print(f"✓ Copied {len(validated_paths)} item(s) to clipboard")
            for path in validated_paths:
                print(f"  - {path}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error during copy operation: {str(e)}")
            return False
    
    def cut(self, paths: List[str]) -> bool:
        """
        Cut files or directories to clipboard (prepare for move operation).
        
        Args:
            paths (List[str]): List of file/directory paths to cut
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Validate all paths exist before cutting
            validated_paths = []
            for path_str in paths:
                path = Path(path_str)
                if not path.exists():
                    print(f"❌ Error: Path does not exist: {path_str}")
                    return False
                validated_paths.append(path.absolute())
            
            # Store paths in clipboard
            self.clipboard = validated_paths
            self.operation_type = OperationType.CUT
            
            print(f"✓ Cut {len(validated_paths)} item(s) to clipboard")
            for path in validated_paths:
                print(f"  - {path}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error during cut operation: {str(e)}")
            return False
    
    def paste(self, destination: str, default_conflict_action: Optional[ConflictAction] = None) -> bool:
        """
        Paste files or directories from clipboard to destination.
        
        Args:
            destination (str): Destination directory path
            default_conflict_action (Optional[ConflictAction]): Default action for conflicts
            
        Returns:
            bool: True if at least one item was pasted successfully, False otherwise
        """
        try:
            # Check if clipboard is empty
            if not self.clipboard:
                print("❌ Error: Clipboard is empty. Please copy or cut files first.")
                return False
            
            # Check if operation type is set
            if self.operation_type is None:
                print("❌ Error: No operation type set.")
                return False
            
            # Validate destination
            dest_path = Path(destination)
            if not dest_path.exists():
                print(f"❌ Error: Destination does not exist: {destination}")
                return False
            
            if not dest_path.is_dir():
                print(f"❌ Error: Destination is not a directory: {destination}")
                return False
            
            # Process each item in clipboard
            success_count = 0
            failed_count = 0
            
            for source_path in self.clipboard:
                try:
                    # Determine destination path
                    dest_item_path = dest_path / source_path.name
                    
                    # Check for conflicts
                    if dest_item_path.exists():
                        action = default_conflict_action or self._ask_conflict_resolution(
                            source_path, dest_item_path
                        )
                        
                        if action == ConflictAction.SKIP:
                            print(f"⊘ Skipped: {source_path.name}")
                            continue
                        elif action == ConflictAction.REPLACE:
                            # Remove existing item
                            if dest_item_path.is_dir():
                                shutil.rmtree(dest_item_path)
                            else:
                                dest_item_path.unlink()
                        elif action == ConflictAction.KEEP_BOTH:
                            # Find a unique name
                            dest_item_path = self._get_unique_name(dest_item_path)
                    
                    # Perform the operation
                    if self.operation_type == OperationType.COPY:
                        self._copy_item(source_path, dest_item_path)
                        print(f"✓ Copied: {source_path.name} -> {dest_item_path}")
                    else:  # CUT
                        self._move_item(source_path, dest_item_path)
                        print(f"✓ Moved: {source_path.name} -> {dest_item_path}")
                    
                    success_count += 1
                    
                except (PermissionError, OSError) as e:
                    print(f"❌ Failed to process {source_path.name}: {str(e)}")
                    failed_count += 1
                except Exception as e:
                    print(f"❌ Unexpected error processing {source_path.name}: {str(e)}")
                    failed_count += 1
            
            # Clear clipboard if it was a cut operation and all items succeeded
            if self.operation_type == OperationType.CUT and failed_count == 0:
                self.clipboard.clear()
                self.operation_type = None
            
            # Print summary
            print(f"\n📊 Summary: {success_count} succeeded, {failed_count} failed")
            
            return success_count > 0
            
        except Exception as e:
            print(f"❌ Error during paste operation: {str(e)}")
            return False
    
    def _copy_item(self, source: Path, destination: Path):
        """
        Copy a single file or directory.
        
        Args:
            source (Path): Source path
            destination (Path): Destination path
            
        Raises:
            FileOperationError: If copy operation fails
        """
        try:
            if source.is_dir():
                shutil.copytree(source, destination, dirs_exist_ok=False)
            else:
                shutil.copy2(source, destination)  # copy2 preserves metadata
        except PermissionError as e:
            raise FileOperationError(f"Permission denied: {str(e)}")
        except OSError as e:
            raise FileOperationError(f"OS error during copy: {str(e)}")
        except Exception as e:
            raise FileOperationError(f"Failed to copy: {str(e)}")
    
    def _move_item(self, source: Path, destination: Path):
        """
        Move a single file or directory.
        
        Args:
            source (Path): Source path
            destination (Path): Destination path
            
        Raises:
            FileOperationError: If move operation fails
        """
        try:
            shutil.move(str(source), str(destination))
        except PermissionError as e:
            raise FileOperationError(f"Permission denied: {str(e)}")
        except OSError as e:
            raise FileOperationError(f"OS error during move: {str(e)}")
        except Exception as e:
            raise FileOperationError(f"Failed to move: {str(e)}")
    
    def _get_unique_name(self, path: Path) -> Path:
        """
        Generate a unique filename by appending (1), (2), etc.
        
        Args:
            path (Path): Original path
            
        Returns:
            Path: Unique path
        """
        parent = path.parent
        stem = path.stem
        suffix = path.suffix
        
        counter = 1
        while True:
            new_name = f"{stem} ({counter}){suffix}"
            new_path = parent / new_name
            if not new_path.exists():
                return new_path
            counter += 1
    
    def _ask_conflict_resolution(self, source: Path, destination: Path) -> ConflictAction:
        """
        Ask user how to resolve file conflict.
        
        Args:
            source (Path): Source path
            destination (Path): Destination path
            
        Returns:
            ConflictAction: User's chosen action
        """
        print(f"\n⚠️  Conflict: '{destination.name}' already exists in destination")
        print(f"   Source: {source}")
        print(f"   Destination: {destination}")
        print("\nChoose an action:")
        print("  [R] Replace - Overwrite the existing file")
        print("  [K] Keep both - Rename the copy (add numbering)")
        print("  [S] Skip - Don't copy/move this file")
        
        while True:
            try:
                choice = input("\nYour choice (R/K/S): ").strip().upper()
                
                if choice == 'R':
                    return ConflictAction.REPLACE
                elif choice == 'K':
                    return ConflictAction.KEEP_BOTH
                elif choice == 'S':
                    return ConflictAction.SKIP
                else:
                    print("❌ Invalid choice. Please enter R, K, or S.")
            except KeyboardInterrupt:
                print("\n\n⊘ Operation cancelled by user.")
                sys.exit(0)
            except Exception as e:
                print(f"❌ Error reading input: {str(e)}")
                return ConflictAction.SKIP
    
    def clear_clipboard(self):
        """Clear the clipboard"""
        self.clipboard.clear()
        self.operation_type = None
        print("✓ Clipboard cleared")
    
    def show_clipboard(self):
        """Display current clipboard contents"""
        if not self.clipboard:
            print("📋 Clipboard is empty")
        else:
            op_type = self.operation_type.value if self.operation_type else "unknown"
            print(f"📋 Clipboard ({op_type}):")
            for path in self.clipboard:
                print(f"  - {path}")


def print_usage():
    """Print usage information"""
    print("""
╔════════════════════════════════════════════════════════════════╗
║           File Operations - Cut, Copy, Paste Script            ║
╚════════════════════════════════════════════════════════════════╝

Usage:
    python file_operations.py <command> [arguments]

Commands:
    copy <path1> [path2] ...    Copy files/folders to clipboard
    cut <path1> [path2] ...     Cut files/folders to clipboard
    paste <destination>         Paste clipboard items to destination
    show                        Show current clipboard contents
    clear                       Clear the clipboard

Examples:
    # Copy files
    python file_operations.py copy file1.txt file2.txt folder1

    # Cut a folder
    python file_operations.py cut /path/to/folder

    # Paste to destination
    python file_operations.py paste /path/to/destination

    # Show clipboard
    python file_operations.py show

    # Clear clipboard
    python file_operations.py clear

Notes:
    - Supports Windows, Linux, Unix, and macOS
    - Preserves file metadata when copying
    - Interactive conflict resolution (replace/keep both/skip)
    - Comprehensive error handling
""")


def main():
    """Main entry point for command-line usage"""
    
    # Create FileOperations instance
    file_ops = FileOperations()
    
    # Check for command-line arguments
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    try:
        if command == "copy":
            if len(sys.argv) < 3:
                print("❌ Error: Please provide at least one path to copy")
                sys.exit(1)
            paths = sys.argv[2:]
            success = file_ops.copy(paths)
            sys.exit(0 if success else 1)
            
        elif command == "cut":
            if len(sys.argv) < 3:
                print("❌ Error: Please provide at least one path to cut")
                sys.exit(1)
            paths = sys.argv[2:]
            success = file_ops.cut(paths)
            sys.exit(0 if success else 1)
            
        elif command == "paste":
            if len(sys.argv) < 3:
                print("❌ Error: Please provide a destination path")
                sys.exit(1)
            destination = sys.argv[2]
            success = file_ops.paste(destination)
            sys.exit(0 if success else 1)
            
        elif command == "show":
            file_ops.show_clipboard()
            sys.exit(0)
            
        elif command == "clear":
            file_ops.clear_clipboard()
            sys.exit(0)
            
        else:
            print(f"❌ Error: Unknown command '{command}'")
            print_usage()
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n⊘ Operation cancelled by user.")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
