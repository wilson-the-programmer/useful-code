package main

import (
	"bufio"
	"fmt"
	"math"
	"os"
	"os/exec"
	"strconv"
	"strings"
)

// ANSI colors
var colors = map[string]string{
	"prompt": "\033[1;36m",
	"output": "\033[1;33m",
	"error":  "\033[1;31m",
	"reset":  "\033[0m",
}

// Evaluate simple arithmetic expressions with + - * / ^ operators
func evalExpression(expr string) (float64, error) {
	expr = strings.ReplaceAll(expr, "^", "**")
	tokens := strings.Fields(expr)
	if len(tokens) == 0 {
		return 0, fmt.Errorf("empty expression")
	}

	stack := []float64{}
	ops := map[string]func(a, b float64) float64{
		"+":  func(a, b float64) float64 { return a + b },
		"-":  func(a, b float64) float64 { return a - b },
		"*":  func(a, b float64) float64 { return a * b },
		"/":  func(a, b float64) float64 { return a / b },
		"**": func(a, b float64) float64 { return math.Pow(a, b) },
	}

	for _, token := range tokens {
		if fn, ok := ops[token]; ok {
			if len(stack) < 2 {
				return 0, fmt.Errorf("invalid expression")
			}
			b := stack[len(stack)-1]
			a := stack[len(stack)-2]
			stack = stack[:len(stack)-2]
			stack = append(stack, fn(a, b))
		} else {
			val, err := strconv.ParseFloat(token, 64)
			if err != nil {
				return 0, fmt.Errorf("invalid number: %s", token)
			}
			stack = append(stack, val)
		}
	}

	if len(stack) != 1 {
		return 0, fmt.Errorf("invalid expression")
	}
	return stack[0], nil
}

// Handle built-in commands like cd
func handleBuiltIn(cmd []string) bool {
	if len(cmd) == 0 {
		return false
	}
	switch cmd[0] {
	case "cd":
		dir := ""
		if len(cmd) > 1 {
			dir = cmd[1]
		} else {
			dir = os.Getenv("HOME")
		}
		if err := os.Chdir(dir); err != nil {
			fmt.Println(colors["error"], "Error:", err, colors["reset"])
		}
		return true
	case "exit":
		os.Exit(0)
	}
	return false
}

func main() {
	reader := bufio.NewReader(os.Stdin)
	history := []string{}

	fmt.Println(colors["output"], "Mini Go Shell (type 'exit' to quit)", colors["reset"])

	for {
		// Prompt
		cwd, _ := os.Getwd()
		fmt.Print(colors["prompt"], cwd, " > ", colors["reset"])

		input, _ := reader.ReadString('\n')
		input = strings.TrimSpace(input)
		if input == "" {
			continue
		}

		history = append(history, input)

		// Attempt arithmetic evaluation first
		if strings.ContainsAny(input, "+-*/^") {
			tokens := strings.Fields(input)
			result, err := evalExpression(strings.Join(tokens, " "))
			if err == nil {
				fmt.Println(colors["output"], result, colors["reset"])
				continue
			}
		}

		// Parse command
		parts := strings.Fields(input)
		if handleBuiltIn(parts) {
			continue
		}

		cmd := exec.Command(parts[0], parts[1:]...)
		cmd.Stdout = os.Stdout
		cmd.Stderr = os.Stderr
		cmd.Stdin = os.Stdin
		if err := cmd.Run(); err != nil {
			fmt.Println(colors["error"], "Error:", err, colors["reset"])
		}
	}
}

