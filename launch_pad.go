package main

import (
    "bufio"
    "fmt"
    "os"
    "os/exec"
    "path/filepath"
    "strings"
    "time"
)

const (
    BoldYellow = "\033[1;33m"
    BoldCyan   = "\033[1;36m"
    BoldOrange = "\033[1;38;5;208m"
    Reset      = "\033[0m"
)

func pause(seconds int) {
    time.Sleep(100 * time.Millisecond)
}

func scanDirectory() []string {
    var programs []string
    entries, err := os.ReadDir(".")
    if err != nil {
        return programs
    }

    for _, entry := range entries {
        if entry.IsDir() {
            continue
        }

        ext := filepath.Ext(entry.Name())
        switch ext {
        case ".go", ".py", ".rs", ".c", ".cpp", ".sh":
            programs = append(programs, entry.Name())
        }
    }
    return programs
}

func buildCommand(file string) *exec.Cmd {
    ext := filepath.Ext(file)
    switch ext {
    case ".go":
        return exec.Command("go", "run", file)
    case ".py":
        return exec.Command("python", file)
    case ".sh":
        return exec.Command("bash", file)
    case ".rs":
        // compile rust and run
        output := strings.TrimSuffix(file, ".rs")
        compile := exec.Command("rustc", file)
        compile.Run()
        return exec.Command("./" + output)
    case ".c":
        output := strings.TrimSuffix(file, ".c")
        compile := exec.Command("gcc", file, "-o", output)
        compile.Run()
        return exec.Command("./" + output)
    case ".cpp":
        output := strings.TrimSuffix(file, ".cpp")
        compile := exec.Command("g++", file, "-o", output)
        compile.Run()
        return exec.Command("./" + output)
    default:
        return nil
    }
}

func main() {
    reader := bufio.NewReader(os.Stdin)

    fmt.Println(BoldCyan + "🌫️  Universal Dev Launcher" + Reset)
    pause(1)

    fmt.Println(BoldYellow + "Scanning current directory..." + Reset)
    pause(1)

    programs := scanDirectory()
    if len(programs) == 0 {
        fmt.Println(BoldYellow + "⚠️  No supported programs found." + Reset)
        return
    }

    fmt.Println(BoldOrange + "\nAvailable Programs:" + Reset)
    pause(1)
    for i, prog := range programs {
        fmt.Printf(BoldCyan+"%d) %s\n"+Reset, i+1, prog)
        pause(1)
    }

    fmt.Print("\n" + BoldYellow + "Enter choice (number): " + Reset)
    input, _ := reader.ReadString('\n')
    input = strings.TrimSpace(input)

    var choice int
    fmt.Sscanf(input, "%d", &choice)

    if choice < 1 || choice > len(programs) {
        fmt.Println(BoldYellow + "\n❌ Invalid selection." + Reset)
        return
    }

    selected := programs[choice-1]

    fmt.Println(BoldCyan + "\n🚀 Launching " + selected + " ..." + Reset)
    pause(1)

    cmd := buildCommand(selected)
    if cmd == nil {
        fmt.Println(BoldYellow + "❌ Unsupported file type." + Reset)
        return
    }

    cmd.Stdin = os.Stdin
    cmd.Stdout = os.Stdout
    cmd.Stderr = os.Stderr

    err := cmd.Run()
    if err != nil {
        fmt.Println(BoldYellow + "\n❌ Error executing program." + Reset)
    }

    fmt.Println(BoldCyan + "\n✨ Done." + Reset)
}
