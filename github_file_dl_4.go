package main

import (
    "bufio"
    "encoding/base64"
    "encoding/json"
    "fmt"
    "io/ioutil"
    "net/http"
    "os"
    "path/filepath"
    "strconv"
    "strings"
    "time"
)

func pause(seconds time.Duration) {
    time.Sleep(seconds * time.Second)
}

func fetchRepos(username, token string) ([]string, error) {
    pause(1)
    fmt.Println("🔍 Fetching repositories...")

    url := fmt.Sprintf("https://api.github.com/users/%s/repos", username)
    req, _ := http.NewRequest("GET", url, nil)
    req.SetBasicAuth(username, token)
    req.Header.Set("Accept", "application/vnd.github+json")

    client := &http.Client{}
    resp, err := client.Do(req)
    if err != nil {
        return nil, err
    }
    defer resp.Body.Close()

    body, _ := ioutil.ReadAll(resp.Body)

    if resp.StatusCode >= 200 && resp.StatusCode < 300 {
        var repos []struct {
            Name string `json:"name"`
        }

        json.Unmarshal(body, &repos)

        repoNames := []string{}
        for _, r := range repos {
            repoNames = append(repoNames, r.Name)
        }

        for i, r := range repoNames {
            fmt.Printf("%d) %s\n", i+1, r)
        }

        return repoNames, nil
    }

    return nil, fmt.Errorf("❌ Failed to fetch repositories:\n%s", string(body))
}

func fetchRepoFiles(username, token, repo, branch string) ([]string, error) {
    pause(1)
    fmt.Println("📂 Fetching files in repository...")

    url := fmt.Sprintf("https://api.github.com/repos/%s/%s/contents?ref=%s", username, repo, branch)
    req, _ := http.NewRequest("GET", url, nil)
    req.SetBasicAuth(username, token)
    req.Header.Set("Accept", "application/vnd.github+json")

    client := &http.Client{}
    resp, err := client.Do(req)
    if err != nil {
        return nil, err
    }
    defer resp.Body.Close()

    body, _ := ioutil.ReadAll(resp.Body)

    if resp.StatusCode >= 200 && resp.StatusCode < 300 {
        var files []struct {
            Name string `json:"name"`
            Type string `json:"type"`
        }

        json.Unmarshal(body, &files)

        fileNames := []string{}
        for _, f := range files {
            if f.Type == "file" {
                fmt.Println("📄", f.Name)
                fileNames = append(fileNames, f.Name)
            } else if f.Type == "dir" {
                fmt.Println("📁", f.Name)
            }
        }

        return fileNames, nil
    }

    return nil, fmt.Errorf("❌ Failed to fetch repository files:\n%s", string(body))
}

func getUniqueFilename(file string) string {
    finalName := file
    count := 1

    for {
        if _, err := os.Stat(finalName); os.IsNotExist(err) {
            break
        }

        ext := filepath.Ext(file)
        name := strings.TrimSuffix(file, ext)
        finalName = fmt.Sprintf("%s(%d)%s", name, count, ext)
        count++
    }

    return finalName
}

func downloadFile(username, token, repo, branch, file string) error {
    pause(1)

    url := fmt.Sprintf("https://api.github.com/repos/%s/%s/contents/%s?ref=%s", username, repo, file, branch)
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
        var result struct {
            Content string `json:"content"`
        }

        json.Unmarshal(body, &result)

        decoded, err := base64.StdEncoding.DecodeString(strings.ReplaceAll(result.Content, "\n", ""))
        if err != nil {
            return err
        }

        finalName := getUniqueFilename(file)

        err = ioutil.WriteFile(finalName, decoded, 0644)
        if err != nil {
            return err
        }

        fmt.Println("✅ Downloaded:", finalName)
        return nil
    }

    return fmt.Errorf("❌ Failed to download %s:\n%s", file, string(body))
}

func main() {
    reader := bufio.NewReader(os.Stdin)

    fmt.Println("💻 Welcome to GitHub File Downloader")
    pause(1)

    fmt.Print("👤 GitHub username: ")
    username, _ := reader.ReadString('\n')
    username = strings.TrimSpace(username)

    fmt.Print("🔑 Personal Access Token: ")
    token, _ := reader.ReadString('\n')
    token = strings.TrimSpace(token)

    repos, err := fetchRepos(username, token)
    if err != nil {
        fmt.Println(err)
        return
    }

    fmt.Print("\nEnter repository number to browse: ")
    choiceStr, _ := reader.ReadString('\n')
    choiceStr = strings.TrimSpace(choiceStr)

    choice, _ := strconv.Atoi(choiceStr)
    if choice < 1 || choice > len(repos) {
        fmt.Println("❌ Invalid repository choice")
        return
    }

    selectedRepo := repos[choice-1]

    fmt.Print("🌿 Branch (main/master, default 'main'): ")
    branch, _ := reader.ReadString('\n')
    branch = strings.TrimSpace(branch)

    branchLower := strings.ToLower(branch)
    if branchLower != "main" && branchLower != "master" {
        branch = "main"
        fmt.Println("➡️ Invalid branch entered. Using default branch: main")
    }

    files, err := fetchRepoFiles(username, token, selectedRepo, branch)
    if err != nil {
        fmt.Println(err)
        return
    }

    if len(files) == 0 {
        fmt.Println("❌ No files found in repository")
        return
    }

    fmt.Print("\nEnter file name(s) to download (comma or space separated): ")
    input, _ := reader.ReadString('\n')
    input = strings.TrimSpace(input)

    selectedFiles := strings.FieldsFunc(input, func(r rune) bool {
        return r == ',' || r == ' '
    })

    fmt.Println("\n⬇️ Starting downloads...")

    for _, fileChoice := range selectedFiles {
        fileChoice = strings.TrimSpace(fileChoice)
        if fileChoice == "" {
            continue
        }

        found := false
        for _, f := range files {
            if f == fileChoice {
                found = true
                break
            }
        }

        if !found {
            fmt.Println("❌ File not found in repository:", fileChoice)
            continue
        }

        err := downloadFile(username, token, selectedRepo, branch, fileChoice)
        if err != nil {
            fmt.Println(err)
        }
    }

    fmt.Println("\n🎉 All downloads complete!")
}