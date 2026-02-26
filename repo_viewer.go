package main

import (
    "bufio"
    "encoding/json"
    "fmt"
    "io/ioutil"
    "net/http"
    "os"
    "strings"
    "time"
)

func pause(seconds time.Duration) {
    time.Sleep(seconds * time.Second)
}

func fetchRepoFiles(username, token, repo, branch string) error {
    pause(1)
    fmt.Println("Fetching file list...")

    url := fmt.Sprintf("https://api.github.com/repos/%s/%s/contents?ref=%s", username, repo, branch)
    req, _ := http.NewRequest("GET", url, nil)
    req.SetBasicAuth(username, token)
    req.Header.Set("Accept", "application/vnd.github+json")

    client := &http.Client{}
    resp, err := client.Do(req)
    if err != nil {
        return err
    }
    defer resp.Body.Close()

    body, _ := ioutil.ReadAll(resp.Body)

    if resp.StatusCode >= 200 && resp.StatusCode < 300 {
        var files []struct {
            Name string `json:"name"`
            Type string `json:"type"`
        }
        json.Unmarshal(body, &files)

        for _, f := range files {
            if f.Type == "file" {
                fmt.Println("📄", f.Name)
            } else if f.Type == "dir" {
                fmt.Println("📁", f.Name)
            }
        }
        fmt.Println("✅ Done! All files displayed.")
    } else {
        fmt.Println("❌ Failed to fetch repository files!")
        fmt.Println(string(body))
    }

    return nil
}

func main() {
    reader := bufio.NewReader(os.Stdin)

    fmt.Println("💻 Welcome to repo_viewer – interactive GitHub repo browser")
    pause(1)

    fmt.Print("GitHub username: ")
    username, _ := reader.ReadString('\n')
    username = strings.TrimSpace(username)

    fmt.Print("Personal Access Token: ")
    token, _ := reader.ReadString('\n')
    token = strings.TrimSpace(token)

    fmt.Print("Repository name: ")
    repo, _ := reader.ReadString('\n')
    repo = strings.TrimSpace(repo)

    fmt.Print("Branch (main/master, default 'main'): ")
    branch, _ := reader.ReadString('\n')
    branch = strings.TrimSpace(branch)
    if branch == "" {
        branch = "main"
    }

    pause(1)
    err := fetchRepoFiles(username, token, repo, branch)
    if err != nil {
        fmt.Println("Error:", err)
    }
}

