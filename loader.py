import os
import subprocess

# Source = folder where this script is located
source_dir = os.path.dirname(os.path.abspath(__file__))

# Destination = Hyprland config folder
dest_dir = os.path.expanduser("~/.config")

# Ensure destination exists
os.makedirs(dest_dir, exist_ok=True)

# Copy everything from source_dir to dest_dir
for item in os.listdir(source_dir):
    s = os.path.join(source_dir, item)
    d = os.path.join(dest_dir, item)

    # Skip copying the script itself if in the same folder
    if os.path.abspath(s) == os.path.abspath(__file__):
        continue

    subprocess.run(["sudo", "cp", "-r", f"{source_dir}/.", dest_dir], check=True)
        

print(f"Copied everything from {source_dir} → {dest_dir}")

try:
    subprocess.run(["hyprctl", "reload"], check=True)
    print("Hyprland config reloaded.")
except subprocess.CalledProcessError as e:
    print(f"Failed to reload Hyprland (command error): {e}")
except FileNotFoundError:
    print("'hyprctl' command not found. Is Hyprland installed and running?")