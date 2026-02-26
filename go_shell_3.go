package main

import (
    "bufio"
    "fmt"
    "math/rand"
    "os"
    "os/exec"
    "sort"
    "strings"
    "time"
)

func randomBrightColor() string {
    r := rand.Intn(106) + 150
    g := rand.Intn(106) + 150
    b := rand.Intn(106) + 150
    return fmt.Sprintf("\033[1;38;2;%d;%d;%dm", r, g, b)
}

func assignUniqueColors(names []string) map[string]string {
    colors := make(map[string]string)
    used := make(map[string]bool)
    for _, n := range names {
        for {
            c := randomBrightColor()
            if !used[c] {
                used[c] = true
                colors[n] = c
                break
            }
        }
    }
    return colors
}

func printFileName(fileName string) {
    fmt.Println()
    fmt.Println("File:", fileName)
    fmt.Println()

}

func main() {
    rand.Seed(time.Now().UnixNano())

    reader := bufio.NewReader(os.Stdin)
    fmt.Print("Enter Go file name: ")
    fileName, _ := reader.ReadString('\n')
    fileName = strings.TrimSpace(fileName)

    file, err := os.Open(fileName)
    if err != nil {
        fmt.Println("Error opening file.")
        return
    }
    defer file.Close()

    rawLines := []string{}
    functionsSet := make(map[string]bool)
    variablesSet := make(map[string]bool)

    scanner := bufio.NewScanner(file)
    for scanner.Scan() {
        line := scanner.Text()
        rawLines = append(rawLines, line)
        trim := strings.TrimSpace(line)

        if strings.HasPrefix(trim, "func ") {
            parts := strings.Fields(trim)
            if len(parts) >= 2 {
                name := strings.Split(parts[1], "(")[0]
                functionsSet[name] = true
            }
        }

        if strings.Contains(line, ":=") &&
            !strings.Contains(line, "if ") &&
            !strings.Contains(line, "for ") {
            parts := strings.Split(line, ":=")
            left := strings.TrimSpace(parts[0])
            if left != "" {
                names := strings.Split(left, ",")
                for _, n := range names {
                    n = strings.TrimSpace(n)
                    if n != "" {
                        variablesSet[n] = true
                    }
                }
            }
        }

        if strings.HasPrefix(trim, "var ") {
            parts := strings.Fields(trim)
            if len(parts) >= 2 {
                variablesSet[parts[1]] = true
            }
        }
    }

    funcList := []string{}
    for f := range functionsSet {
        funcList = append(funcList, f)
    }
    sort.Strings(funcList)

    varList := []string{}
    for v := range variablesSet {
        varList = append(varList, v)
    }
    sort.Strings(varList)

    funcColors := assignUniqueColors(funcList)
    varColors := assignUniqueColors(varList)

    boldOrange := "\033[1;38;2;255;165;0m"
    boldCyan := "\033[1;38;2;0;255;255m"
    reset := "\033[0m"

    printFileName(fileName)

    for {
        fmt.Print("> ")
        input, _ := reader.ReadString('\n')
        input = strings.TrimSpace(input)
        if input == "" {
            continue
        }
        if input == "q" || input == "exit" {
            break
        }

        // List variables
        if input == "list var" {
            fmt.Println()
            fmt.Println("Variables:")
            for _, v := range varList {
                fmt.Println("    " + varColors[v] + v + reset)
            }
            printFileName(fileName)
            continue
        }

        // List functions
        if input == "list func" {
            fmt.Println()
            fmt.Println("Functions:")
            for _, f := range funcList {
                fmt.Println("    " + funcColors[f] + f + reset)
            }
            printFileName(fileName)
            continue
        }

        // System commands
        if _, err := exec.LookPath(strings.Fields(input)[0]); err == nil {
            cmdParts := strings.Fields(input)
            cmd := exec.Command(cmdParts[0], cmdParts[1:]...)
            cmd.Dir = "/root/"
            cmd.Stdout = os.Stdout
            cmd.Stderr = os.Stderr
            cmd.Run()
            printFileName(fileName)
            continue
        }

        // Function with N lines below
        if strings.Contains(input, ",") {
            parts := strings.Split(input, ",")
            funcName := strings.TrimSpace(parts[0])
            linesBelow := 0
            fmt.Sscanf(parts[1], "%d", &linesBelow)

            for i, line := range rawLines {
                if strings.HasPrefix(strings.TrimSpace(line), "func "+funcName) {
                    end := i + linesBelow + 1
                    if end > len(rawLines) {
                        end = len(rawLines)
                    }
                    highlight := strings.Replace(line, funcName, boldCyan+funcName+reset, 1)
                    fmt.Printf("%3d. %s\n", i+1, highlight)
                    for j := i + 1; j < end; j++ {
                        fmt.Printf("%3d. %s\n", j+1, rawLines[j])
                    }
                }
            }
            printFileName(fileName)
            continue
        }

        // Variable search
        found := false
        for i, line := range rawLines {
            if strings.HasPrefix(strings.TrimSpace(line), "var "+input) ||
                (strings.Contains(line, ":=") && strings.HasPrefix(strings.TrimSpace(line), input+" ")) {
                parts := strings.Split(line, input)
                fmt.Printf("%3d. %s%s%s%s\n", i+1, parts[0], boldOrange, input, reset+parts[1])
                found = true
                break
            }
        }
        if !found {
            fmt.Println("Variable or function not found in file.")
        }
        printFileName(fileName)
    }
}
