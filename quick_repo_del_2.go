
package main

import (
    "bufio"
    "encoding/json"
    "fmt"
    "net/http"
    "os"
    "strings"
    "time"
)

func pause(duration time.Duration) {
    time.Sleep(duration)
}

func deleteRepository(username, token, repo string) error {
    pause(500 * time.Millisecond)
    fmt.Println("Deleting repository...")

    url := fmt.Sprintf("https://api.github.com/repos/%s/%s", username, repo)

    req, err := http.NewRequest("DELETE", url, nil)
    if err != nil {
        return err
    }

    req.SetBasicAuth(username, token)
    req.Header.Set("Accept", "application/vnd.github+json")

    client := &http.Client{}
    resp, err := client.Do(req)
    if err != nil {
        return err
    }
    defer resp.Body.Close()

    if resp.StatusCode == http.StatusNoContent {
        fmt.Println("✅ Repository deleted successfully!")
        fmt.Println("📦 Repository:", repo)
        return nil
    }

    var errorResult struct {
        Message string `json:"message"`
    }

    json.NewDecoder(resp.Body).Decode(&errorResult)

    fmt.Println("❌ Failed to delete repository!")

    if errorResult.Message != "" {
        fmt.Println("GitHub:", errorResult.Message)
    }

    return nil
}

func main() {
    reader := bufio.NewReader(os.Stdin)

    fmt.Println("💻 Welcome to repo_delete – GitHub repository deleter")

    pause(500 * time.Millisecond)
    fmt.Print("GitHub username: ")
    username, _ := reader.ReadString('\n')
    username = strings.TrimSpace(username)

    pause(500 * time.Millisecond)
    fmt.Print("Personal Access Token: ")
    token, _ := reader.ReadString('\n')
    token = strings.TrimSpace(token)

    pause(500 * time.Millisecond)
    fmt.Print("Repository name(s): ")
    repositoryInput, _ := reader.ReadString('\n')

    repositories := strings.Split(repositoryInput, ",")

    for _, repo := range repositories {
        repo = strings.TrimSpace(repo)

        if repo == "" {
            continue
        }

        pause(500 * time.Millisecond)
        fmt.Printf("Delete repository '%s'? (yes/no): ", repo)

        confirmation, _ := reader.ReadString('\n')
        confirmation = strings.ToLower(strings.TrimSpace(confirmation))

        if confirmation != "yes" {
            fmt.Println("❌ Skipped:", repo)
            continue
        }

        err := deleteRepository(username, token, repo)
        if err != nil {
            fmt.Println("Error:", err)
        }

        fmt.Println()
    }
}

