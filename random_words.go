package main

import (
    "fmt"
    "math/rand"
    "time"
)

func quick_color() (string, int, int, int, string) {
    r := 140 + rand.Intn(86)
    g := 140 + rand.Intn(86)
    b := 140 + rand.Intn(86)
    hex := fmt.Sprintf("#%02X%02X%02X", r, g, b)
    rgbCode := fmt.Sprintf("\033[1;38;2;%d;%d;%dm", r, g, b)
    return rgbCode, r, g, b, hex
}

func main() {
    rand.Seed(time.Now().UnixNano())

    keywords := []string{
        "break",
        "case",
        "chan",
        "const",
        "continue",
        "default",
        "defer",
        "else",
        "fallthrough",
        "for",
        "func",
        "go",
        "goto",
        "if",
        "import",
        "interface",
        "map",
        "package",
        "range",
        "return",
        "select",
        "struct",
        "switch",
        "type",
        "var",
    }

    var maxPrints int
    fmt.Print("Amount of colors: ")
    fmt.Scan(&maxPrints)

    for i := 0; i < maxPrints; i++ {
        word := keywords[i%len(keywords)]
        color, r, g, b, hex := quick_color()
        fmt.Printf("%s%s  → (%d, %d, %d),  '%s'\033[0m\n", color, word, r, g, b, hex)
        time.Sleep(1 * time.Second)
    }
}
