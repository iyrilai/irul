#!/bin/bash

# Get info about the active window
window_info=$(hyprctl activewindow -j)
is_floating=$(echo "$window_info" | jq -r '.floating')
window_address=$(echo "$window_info" | jq -r '.address')
current_workspace_id=$(echo "$window_info" | jq -r '.workspace.id')

# Count tiled windows on the current desktop
tiled_window_count=$(hyprctl clients -j | jq --argjson ws_id "$current_workspace_id" '.[] | select(.workspace.id == $ws_id and .floating == false)' | jq -s 'length')

# Logic for the toggle function
if [ "$is_floating" = "true" ]; then
    # Case 1: Window is floating, so toggle it to auto tile
    hyprctl dispatch togglefloating
else
    # Window is auto tiled
    if [ "$tiled_window_count" -eq 1 ]; then
        # Case 2: Auto tiled and is the only window
        # Make it floating
        
        # Close the current desktop by moving to a different one
        # This will remove the now-empty workspace.
        hyprctl dispatch movetoworkspace "name:next_workspace"
        hyprctl dispatch togglefloating
        
    else
        # Case 3: Auto tiled but with other windows
        # Create a new workspace and move the window to it
        # The window will remain tiled on the new desktop
        hyprctl dispatch movetoworkspace "name:new_desktop"
    fi
fi