#!/bin/env bash
export DIALOGRC=$(mktemp)
cat <<EOF > $DIALOGRC
# Set dialog default colors                        
screen_color = (WHITE,BLACK,ON)
title_color  = (WHITE,BLUE,ON)
shadow_color = (BLACK,BLACK,OFF)
border_color = (WHITE,BLACK,ON)
EOF

HEIGHT=$(tput lines)
WIDTH=$(tput cols)
DIR="."

while true; do
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

    CHOICE=$(dialog --clear --title "File Explorer: $DIR" \
        --menu "Choose a file or directory" $HEIGHT $WIDTH $((HEIGHT-4)) \
        "${FILES[@]}" \
        3>&1 1>&2 2>&3)

    [ $? -ne 0 ] && break

    SELECTED="$DIR/$CHOICE"

    if [ -d "$SELECTED" ]; then
        DIR="$SELECTED"
    else
        dialog --title "$CHOICE" --textbox "$SELECTED" $HEIGHT $WIDTH
    fi                                             done

rm -f $DIALOGRC
clear