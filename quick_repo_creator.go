
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

func createRepository(username, token, repo, description, visibility string) error {
    pause(500 * time.Millisecond)
    fmt.Println("Creating repository...")

    url := "https://api.github.com/user/repos"

    data := map[string]interface{}{
        "name":        repo,
        "description": description,
        "private":     visibility == "private",
    }

    jsonData, err := json.Marshal(data)
    if err != nil {
        return err
    }

    req, err := http.NewRequest("POST", url, strings.NewReader(string(jsonData)))
    if err != nil {
        return err
    }

    req.SetBasicAuth(username, token)
    req.Header.Set("Accept", "application/vnd.github+json")
    req.Header.Set("Content-Type", "application/json")

    client := &http.Client{}
    resp, err := client.Do(req)
    if err != nil {
        return err
    }
    defer resp.Body.Close()

    if resp.StatusCode >= 200 && resp.StatusCode < 300 {
        var result struct {
            Name string `json:"name"`
            URL  string `json:"html_url"`
        }

        err := json.NewDecoder(resp.Body).Decode(&result)
        if err != nil {
            return err
        }

        fmt.Println()
        fmt.Println("✅ Repository created successfully!")
        fmt.Println("📦 Repository:", result.Name)
        fmt.Println("🔗", result.URL)

        return nil
    }

    var errorResult struct {
        Message string `json:"message"`
    }

    json.NewDecoder(resp.Body).Decode(&errorResult)

    fmt.Println()
    fmt.Println("❌ Failed to create repository!")
    fmt.Println("GitHub:", errorResult.Message)

    return nil
}

func main() {
    reader := bufio.NewReader(os.Stdin)

    fmt.Println("💻 Welcome to repo_creator – GitHub repository creator")

    pause(500 * time.Millisecond)
    fmt.Print("GitHub username: ")
    username, _ := reader.ReadString('\n')
    username = strings.TrimSpace(username)

    pause(500 * time.Millisecond)
    fmt.Print("Personal Access Token: ")
    token, _ := reader.ReadString('\n')
    token = strings.TrimSpace(token)

    pause(500 * time.Millisecond)
    fmt.Print("Repository name: ")
    repo, _ := reader.ReadString('\n')
    repo = strings.TrimSpace(repo)

    pause(500 * time.Millisecond)
    fmt.Print("Description: ")
    description, _ := reader.ReadString('\n')
    description = strings.TrimSpace(description)

    pause(500 * time.Millisecond)
    fmt.Print("Visibility (public/private): ")
    visibility, _ := reader.ReadString('\n')
    visibility = strings.ToLower(strings.TrimSpace(visibility))

    if visibility != "private" {
        visibility = "public"
    }

    pause(500 * time.Millisecond)

    err := createRepository(username, token, repo, description, visibility)
    if err != nil {
        fmt.Println("Error:", err)
    }
}

