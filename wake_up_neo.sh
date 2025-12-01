

#!/usr/bin/env bash

SPEED=0.05      # seconds between letters
BIT_SPEED=0.02   # seconds between bits
PAUSE=2

text=(
    "Wake up Neo..."
    "The matrix has you..."
    "Follow the White rabbit."
    "Knock Knock."
)

# Function to generate mostly green RGB color
random_green() {
    R=$(( RANDOM % 50 ))       # small red component
    G=$(( 150 + RANDOM % 106 )) # strong green component
    B=$(( RANDOM % 50 ))       # small blue component
    echo "\033[38;2;${R};${G};${B}m"
}

GREEN_BOLD=$'\033[1;32m'
RESET=$'\033[0m'

# Three new lines
printf "\n\n\n"

# Slow-print text
for sentence in "${text[@]}"; do
    printf "\t"
    for ((i=0; i<${#sentence}; i++)); do
        printf "%s" "${GREEN_BOLD}${sentence:$i:1}${RESET}"
        sleep "$SPEED"
    done
    printf "\n"
    sleep "$PAUSE"
done

# Four new lines before binary
printf "\n\n\n\n"

# Print binary square with random greenish bits
for sentence in "${text[@]}"; do
    printf "\t"
    for ((i=0; i<${#sentence}; i++)); do
        char="${sentence:$i:1}"
        bin=$(echo "obase=2; $(printf '%d' "'$char")" | bc)
        # Ensure 8-bit
        bin=$(printf "%08d" "$bin")
        for ((b=0; b<${#bin}; b++)); do
            color=$(random_green)
            printf "${color}%s${RESET}" "${bin:$b:1}"
            sleep "$BIT_SPEED"
        done
        printf " "
    done
    printf "\n"
done



