#!/usr/bin/env bash

FILES=()
i=1

for f in $(ls -1 | sort); do
    case "$f" in
        *.py|*.sh|*.c|*.cpp|*.js)
            [ -f "$f" ] && FILES+=("$i" "$f") && i=$((i+1))
            ;;
    esac
done

if [ ${#FILES[@]} -eq 0 ]; then
    dialog --msgbox "No runnable files found." 10 40
    clear
    exit 1
fi

CHOICE=$(dialog --stdout --title "Choose a file to run" \
    --menu "Select:" 20 60 15 "${FILES[@]}")

if [ -z "$CHOICE" ]; then
    clear
    exit 0
fi

FILE=$(echo "${FILES[@]}" | tr ' ' '\n' | grep -A1 "$CHOICE" | tail -n1)

clear
EXT="${FILE##*.}"

case "$EXT" in
    py) python "$FILE" ;;
    sh) bash "$FILE" ;;
    c)  gcc "$FILE" -o a.out && ./a.out ;;
    cpp) g++ "$FILE" -o a.out && ./a.out ;;
    js) node "$FILE" ;;
esac

echo
read -p "Press ENTER to return to menu..."

