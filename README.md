# PurgeScriptsLinux

This repository contains system maintenance and cleanup scripts for Linux environments.

## Scripts

### [archive.ksh](./archive.ksh)

A KornShell script designed to automate the archiving and deletion of old files to save disk space and maintain hygiene.

**Key Features:**
1.  **Log Cleanup**: Deletes `*.log` files older than 90 days.
2.  **DB Backup Check**: Archives (tars) `*.bak` files and moves them to a remote NAS (`/mnt/DBBKPVgs`).
3.  **Tmp Cleanup**: Deletes `*.tmp` files older than 30 days.
4.  **RECU File Handling**: Archives (tars) `*.RECU` files and moves them to a disk mount (`/mnt/disk_mount`).

**Configuration:**
The script has configurable variables at the top for search paths and file patterns:
- `LOG_SEARCH_PATH`, `DB_BACKUP_SEARCH_PATH`, etc.
- `NAS_MOUNT_POINT`, `DISK_MOUNT_POINT`

## Manual Testing Steps

To safely test the `archive.ksh` script in a new environment, follow these steps:

### 1. Dry Run (Recommended)
Before running the script in production, modify it to print actions instead of executing them.
- Open `archive.ksh`.
- Replace `rm "$file"` with `echo "Deleting $file"`.
- Replace `mv "$ARCHIVE_NAME" ...` with `echo "Moving $ARCHIVE_NAME..."`.

### 2. Create Test Data
Create dummy files to verify the script identifies the correct files based on age and extension.

```bash
# Create a log file older than 90 days (should be deleted)
touch -d "91 days ago" old_log.log

# Create a log file newer than 90 days (should NOT be deleted)
touch -d "89 days ago" new_log.log

# Create a dummy backup file (should be archived)
touch db_backup.bak

# Create an old tmp file (should be deleted)
touch -d "31 days ago" old_tmp.tmp

# Create a dummy RECU file (should be archived)
touch data.RECU
```

### 3. Run the Script
Execute the script and observe the output.

```bash
chmod +x archive.ksh
./archive.ksh
```

### 4. Verify Results
- **Check Deletion**: `old_log.log` and `old_tmp.tmp` should be gone. `new_log.log` should remain.
- **Check Archival**:
    - A tarball containing `db_backup.bak` should exist in the configured NAS path.
    - A tarball containing `data.RECU` should exist in the configured Disk Mount path.
