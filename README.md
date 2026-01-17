# PurgeScriptsLinux

This repository contains system maintenance and cleanup scripts for Linux environments, as well as educational scripts for various programming languages.

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

### [CoffeeScriptDemo.coffee](./CoffeeScriptDemo.coffee)

A comprehensive, runnable demonstration of CoffeeScript features, serving as both a guide and a test script.

**Key Features:**
- **Syntax Showcase**: Demonstrates whitespace significance, string interpolation, and "it's just JavaScript" philosophy.
- **Functional Patterns**: Covers functions, default arguments, and the "fat arrow" (`=>`) for context binding.
- **Data Structures**: Detailed examples of objects (YAML-style), arrays, and ranges.
- **Control Flow**: Illustrates idiomatic `if`/`unless` modifiers and `switch` statements.
- **Advanced Features**: Splats (`...`), destructuring assignment, and the existential operator (`?`).

### [KotlinBasics.kt](./KotlinBasics.kt)

A tutorial file illustrating the fundamental building blocks of the Kotlin language, focusing on safety and conciseness.

**Key Features:**
- **Type System**: Contrasts `val` (immutable) vs `var` (mutable) and demonstrates type inference.
- **Control Flow**: Explains `if` as an expression and the powerful `when` construct.
- **Null Safety**: Demonstrates safe calls (`?.`) and the Elvis operator (`?:`) to handle nullability.
- **OOP**: Shows Class and Data Class definitions.
- **Entry Point**: Includes a `main()` function that executes all examples.

### [file_operations.py](./file_operations.py)

A robust, cross-platform Python utility script that mimics Windows Explorer's Cut, Copy, and Paste functionality.

**Key Features:**
- **Clipboard Simulation**: Manages a file list and operation type (Cut vs Copy) in memory.
- **Conflict Resolution**: Interactive prompts to [R]eplace, [K]eep both (auto-numbered), or [S]kip conflicting files.
- **Safety**: Extensive exception handling for permissions and OS errors.
- **CLI Interface**: Easy-to-use command structure (`copy <files>`, `paste <dest>`, `show`).

### [ruby_basics.rb](./ruby_basics.rb)

A clear, commented guide to the core concepts of the Ruby programming language.

**Key Features:**
- **Dynamic Typing**: Demonstrates Ruby's flexible variable system.
- **Blocks & Iterators**: Shows the power of `.each`, `.times`, and standard loops.
- **OOP First**: Explains how everything is an object, including Class definitions and methods.
- **Flow Control**: Covers standard `if/elsif` along with the idiomatic `case` and `unless` statements.

### [GroovyDemo.groovy](./GroovyDemo.groovy)

A comprehensive guide to the Groovy programming language, highlighting its dynamic features and seamless Java integration.

**Key Features:**
- **Closures**: Explains Groovy's defining feature for functional programming and custom DSLs.
- **Collections**: Native syntax for Lists and Maps with powerful iteration methods (`each`, `findAll`).
- **POGOs**: Plain Old Groovy Objects with auto-generated getters/setters and named constructors.
- **Advanced Syntax**: Null-safe navigation (`?.`), Elvis operator (`?:`), and dynamic `Expando` objects.
- **Ecosystem Guide**: Details Groovy's popularity in **Gradle** builds, **Jenkins** pipelines, and **Spock** testing.

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
