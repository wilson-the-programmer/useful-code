#!/bin/bash

# Get terminal size
HEIGHT=$(tput lines)
WIDTH=$(tput cols)

# Starting directory
DIR="${1:-.}"

while true; do
    # Build the menu of files/folders
    FILES=()
    for f in "$DIR"/*; do
        [ -e "$f" ] || continue
        BASENAME=$(basename "$f")
        if [ -d "$f" ]; then
            FILES+=("$BASENAME" "DIR")
        else
            FILES+=("$BASENAME" "FILE")
        fi
    done

    # Show menu
    CHOICE=$(dialog --clear --title "File Explorer: $DIR" \
        --menu "Choose a file or directory" $HEIGHT $WIDTH $((HEIGHT-4)) \
        "${FILES[@]}" \
        3>&1 1>&2 2>&3)

    # Cancel or ESC
    [ $? -ne 0 ] && break

    SELECTED="$DIR/$CHOICE"

    if [ -d "$SELECTED" ]; then
        DIR="$SELECTED"  # enter directory
    else
        # View file in a new dialog window
        dialog --title "$CHOICE" --textbox "$SELECTED" $HEIGHT $WIDTH
    fi
done

clear
