#!/bin/bash


echo
echo

echo "Lines:    Words:    Bytes:    File:"
echo "--------------------------------------"
echo

total_lines=0
total_words=0
total_bytes=0

if [ $# -eq 0 ]; then
    echo "Usage: $0 file1 [file2 ...]"
    exit 1
fi

for file in "$@"; do
    if [ ! -f "$file" ]; then
        echo "Not a file: $file"
        continue
    fi

    read lines words bytes _ < <(wc "$file")
    printf " %3d     %5d     %6d     %s
" "$lines" "$words" "$bytes" "$file"

    ((total_lines += lines))
    ((total_words += words))
    ((total_bytes += bytes))
done

echo
printf " %3d     %5d     %6d     TOTAL
" "$total_lines" "$total_words" "$total_bytes"
echo
echo