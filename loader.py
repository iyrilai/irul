#!/usr/bin/env python3
# loader.py

import os
import shutil

def sync_directory(source_dir_name: str, base_destination_dir: str):
    """
    Synchronizes a source directory to a destination, making the destination
    an exact mirror.

    - Copies new/modified files from source to destination.
    - Deletes files from destination that are not in the source.
    - Creates necessary subdirectories in the destination.
    - Cleans up empty subdirectories in the destination.

    Args:
        source_dir_name (str): The name of the directory to sync (e.g., 'hypr').
        base_destination_dir (str): The parent destination directory (e.g., '~/.config').
    """
    # --- 1. Define Paths ---
    script_location = os.path.dirname(os.path.abspath(__file__))
    source_path = os.path.join(script_location, source_dir_name)
    destination_path = os.path.join(os.path.expanduser(base_destination_dir), source_dir_name)

    print(f"Source:      {source_path}")
    print(f"Destination: {destination_path}\n")

    # --- 2. Pre-flight Checks ---
    # This check is good practice, though our main loop already ensures it's a dir.
    if not os.path.isdir(source_path):
        print(f"Error: Source directory '{source_path}' not found. Aborting.")
        return

    os.makedirs(destination_path, exist_ok=True)
    print("Ensured destination directory exists.")

    # --- 3. Sync from Source to Destination (Copy/Update) ---
    print("\n--- Syncing files to destination ---")
    source_files = set()
    for dirpath, _, filenames in os.walk(source_path):
        for filename in filenames:
            source_file_path = os.path.join(dirpath, filename)
            relative_path = os.path.relpath(source_file_path, source_path)
            source_files.add(relative_path)
            
            destination_file_path = os.path.join(destination_path, relative_path)
            os.makedirs(os.path.dirname(destination_file_path), exist_ok=True)
            
            shutil.copy2(source_file_path, destination_file_path)
            print(f"  -> Copied: {relative_path}")

    # --- 4. Clean Destination (Delete Extra Files) ---
    print("\n--- Cleaning extraneous files from destination ---")
    files_deleted = False
    for dirpath, _, filenames in os.walk(destination_path):
        for filename in filenames:
            destination_file_path = os.path.join(dirpath, filename)
            relative_path = os.path.relpath(destination_file_path, destination_path)
            
            if relative_path not in source_files:
                os.remove(destination_file_path)
                files_deleted = True
                print(f"  -> Deleted: {relative_path}")

    if not files_deleted:
        print("  -> No extraneous files to delete.")

    # --- 5. Clean Destination (Delete Empty Subdirectories) ---
    for dirpath, _, _ in os.walk(destination_path, topdown=False):
        if not os.listdir(dirpath):
            try:
                os.rmdir(dirpath)
                print(f"  -> Removed empty directory: {dirpath}")
            except OSError as e:
                print(f"  -> Warning: Could not remove {dirpath}: {e}")
    
    print("\n✨ Sync complete for this directory.")


if __name__ == "__main__":
    # The destination parent directory. '~' will be expanded to the user's home.
    DESTINATION_PARENT_DIR = "~/.config"
    
    # Get the directory where this script is located.
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    print(f"🚀 Starting sync process...\nScanning for directories in: {script_dir}\n")

    # --- Automatically find and sync all valid directories ---
    synced_anything = False
    for item_name in os.listdir(script_dir):
        full_path = os.path.join(script_dir, item_name)
        
        # We only want to sync items that are directories.
        # We also ignore hidden directories (like .git) and python caches.
        if os.path.isdir(full_path) and not item_name.startswith('.') and item_name != "__pycache__":
            print(f"--- Found directory to sync: '{item_name}' ---")
            sync_directory(item_name, DESTINATION_PARENT_DIR)
            print("-" * (len(item_name) + 30)) # Separator line
            synced_anything = True

    if not synced_anything:
        print("No directories found to sync in the script's location.")
    else:
        print("All tasks complete.")#!/usr/bin/env python3
# loader.py

import os
import shutil

def sync_directory(source_dir_name: str, base_destination_dir: str):
    # --- 1. Define Paths ---
    # Get the directory where this script is located
    script_location = os.path.dirname(os.path.abspath(__file__))
    
    # Construct the full source and destination paths
    source_path = os.path.join(script_location, source_dir_name)
    destination_path = os.path.join(os.path.expanduser(base_destination_dir), source_dir_name)

    print(f"Source:      {source_path}")
    print(f"Destination: {destination_path}\n")

    # --- 2. Pre-flight Checks ---
    # Exit if the source directory doesn't exist
    if not os.path.isdir(source_path):
        print(f"Error: Source directory '{source_path}' not found. Aborting.")
        return

    # Create the base destination directory if it doesn't exist
    os.makedirs(destination_path, exist_ok=True)
    print(f"Ensured destination directory exists.")

    # --- 3. Sync from Source to Destination (Copy/Update) ---
    print("\n--- Syncing files to destination ---")
    source_files = set()
    for dirpath, _, filenames in os.walk(source_path):
        for filename in filenames:
            # Get the full path of the source file
            source_file_path = os.path.join(dirpath, filename)
            
            # Get the file's path relative to the source directory's root
            relative_path = os.path.relpath(source_file_path, source_path)
            source_files.add(relative_path)
            
            # Construct the corresponding destination file path
            destination_file_path = os.path.join(destination_path, relative_path)
            
            # Create the subdirectories in the destination if they don't exist
            os.makedirs(os.path.dirname(destination_file_path), exist_ok=True)
            
            # Copy the file, overwriting if it exists. copy2 preserves metadata.
            shutil.copy2(source_file_path, destination_file_path)
            print(f"  -> Copied: {relative_path}")

    # --- 4. Clean Destination (Delete Extra Files) ---
    print("\n--- Cleaning extraneous files from destination ---")
    files_deleted = False
    for dirpath, _, filenames in os.walk(destination_path):
        for filename in filenames:
            destination_file_path = os.path.join(dirpath, filename)
            relative_path = os.path.relpath(destination_file_path, destination_path)
            
            # If a file in the destination is NOT in our set of source files, delete it.
            if relative_path not in source_files:
                os.remove(destination_file_path)
                files_deleted = True
                print(f"  -> Deleted: {relative_path}")

    if not files_deleted:
        print("  -> No extraneous files to delete.")

    # --- 5. Clean Destination (Delete Empty Subdirectories) ---
    # Walk the tree from the bottom up to remove now-empty folders
    for dirpath, _, _ in os.walk(destination_path, topdown=False):
        # Check if the directory is empty
        if not os.listdir(dirpath):
            os.rmdir(dirpath)
            print(f"  -> Removed empty directory: {dirpath}")

    print("\n✨ Sync complete.")


if __name__ == "__main__":
    # The name of the folder in the current directory you want to copy
    SOURCE_DIRECTORY_NAME = "hypr"
    
    # The destination parent directory. '~' will be expanded to the user's home.
    DESTINATION_PARENT_DIR = "~/.config"
    
    sync_directory(SOURCE_DIRECTORY_NAME, DESTINATION_PARENT_DIR)