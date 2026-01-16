#!/bin/ksh

# -----------------------------------------------------------------------------
# Script Name: archive.ksh
# Purpose: 
#   1. Delete Log files older than 90 days.
#   2. Tar DB Backups and move to remote NAS (DBBKPVgs).
#   3. Delete tmp files older than 30 days.
#   4. Tar .RECU files and move to empty Disk Mount.
#
# Usage: ./archive.ksh
# -----------------------------------------------------------------------------

# --- Configuration Variables ---
# Update these paths according to the actual environment
LOG_SEARCH_PATH="/"           # Where to search for log files
DB_BACKUP_SEARCH_PATH="/"     # Where to search for DB backups
TMP_SEARCH_PATH="/"           # Where to search for tmp files
RECU_SEARCH_PATH="/"          # Where to search for .RECU files

NAS_MOUNT_POINT="/mnt/DBBKPVgs"
DISK_MOUNT_POINT="/mnt/disk_mount"

# File Patterns
LOG_PATTERN="*.log"
DB_BACKUP_PATTERN="*.bak"     # Adjust extension as needed (e.g., *.sql, *.dmp)
TMP_PATTERN="*.tmp"
RECU_PATTERN="*.RECU"

# Timestamp for Archive Names
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# -----------------------------------------------------------------------------
# 1. Delete Log files older than 90 days
# -----------------------------------------------------------------------------
echo "Starting cleanup of Log files older than 90 days..."

# Check if any such files exist to avoid error messages
# We use find to locate the files. 
# 2>/dev/null suppresses permission denied errors which are common when searching /
find "$LOG_SEARCH_PATH" -name "$LOG_PATTERN" -type f -mtime +90 2>/dev/null | while read -r file; do
    if [[ -f "$file" ]]; then
        echo "Deleting log file: $file"
        rm "$file"
    fi
done

echo "Log cleanup complete."

# -----------------------------------------------------------------------------
# 2. Tar any DB Backups and move to a remote NAS named DBBKPVgs
# -----------------------------------------------------------------------------
echo "Checking for DB Backups to archive..."

# Create a temporary list of files
DB_FILES_LIST="/tmp/db_files_to_archive_$TIMESTAMP.txt"
find "$DB_BACKUP_SEARCH_PATH" -name "$DB_BACKUP_PATTERN" -type f 2>/dev/null > "$DB_FILES_LIST"

if [[ -s "$DB_FILES_LIST" ]]; then
    ARCHIVE_NAME="db_backups_$TIMESTAMP.tar.gz"
    echo "Found DB backups. Creating archive $ARCHIVE_NAME..."
    
    # Create tar archive from file list
    # -T reads files from the list
    tar -czf "$ARCHIVE_NAME" -T "$DB_FILES_LIST"
    
    if [[ $? -eq 0 ]]; then
        echo "Archive created successfully. Moving to $NAS_MOUNT_POINT..."
        
        # Ensure destination exists
        if [[ ! -d "$NAS_MOUNT_POINT" ]]; then
            echo "WARNING: NAS Mount point $NAS_MOUNT_POINT does not exist. Attempting to create or failing safely."
            # Depending on policy, might try mkdir or just exit. 
            # For now, we report error and don't delete source files.
        else
            mv "$ARCHIVE_NAME" "$NAS_MOUNT_POINT/"
            if [[ $? -eq 0 ]]; then
                echo "Move successful."
                # Optional: Delete source files after successful move? 
                # "Tar... and move" usually implies archiving off the system.
                # Uncomment the following lines to delete source files after archiving:
                # echo "Removing source files..."
                # while read -r file; do rm "$file"; done < "$DB_FILES_LIST"
            else
                echo "Error moving archive to NAS."
            fi
        fi
    else
        echo "Error creating tar archive for DB backups."
    fi
else
    echo "No DB Backups found."
fi
rm -f "$DB_FILES_LIST"

# -----------------------------------------------------------------------------
# 3. Delete tmp files older than 30 days
# -----------------------------------------------------------------------------
echo "Starting cleanup of tmp files older than 30 days..."

find "$TMP_SEARCH_PATH" -name "$TMP_PATTERN" -type f -mtime +30 2>/dev/null | while read -r file; do
    if [[ -f "$file" ]]; then
        echo "Deleting tmp file: $file"
        rm "$file"
    fi
done

echo "Tmp file cleanup complete."

# -----------------------------------------------------------------------------
# 4. Will tar .RECU files and move them to an empty Disk Mount
# -----------------------------------------------------------------------------
echo "Checking for .RECU files to archive..."

RECU_FILES_LIST="/tmp/recu_files_to_archive_$TIMESTAMP.txt"
find "$RECU_SEARCH_PATH" -name "$RECU_PATTERN" -type f 2>/dev/null > "$RECU_FILES_LIST"

if [[ -s "$RECU_FILES_LIST" ]]; then
    RECU_ARCHIVE_NAME="recu_files_$TIMESTAMP.tar.gz"
    echo "Found .RECU files. Creating archive $RECU_ARCHIVE_NAME..."
    
    tar -czf "$RECU_ARCHIVE_NAME" -T "$RECU_FILES_LIST"
    
    if [[ $? -eq 0 ]]; then
        echo "Archive created successfully. Moving to $DISK_MOUNT_POINT..."
        
        if [[ ! -d "$DISK_MOUNT_POINT" ]]; then
            echo "WARNING: Disk Mount point $DISK_MOUNT_POINT does not exist."
        else
            # Check if mount is empty (optional based on "empty Disk Mount" description? 
            # Or does it mean "a mount reserved for this"? assuming target dir.)
            mv "$RECU_ARCHIVE_NAME" "$DISK_MOUNT_POINT/"
            if [[ $? -eq 0 ]]; then
                echo "Move successful."
                # Optional: Delete source files
                # echo "Removing source files..."
                # while read -r file; do rm "$file"; done < "$RECU_FILES_LIST"
            else
                echo "Error moving archive to disk mount."
            fi
        fi
    else
        echo "Error creating tar archive for .RECU files."
    fi
else
    echo "No .RECU files found."
fi
rm -f "$RECU_FILES_LIST"

echo "Script execution finished."
