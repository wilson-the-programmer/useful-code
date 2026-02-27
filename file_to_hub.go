// file uploader

package main

import (
    "bufio"
    "encoding/base64"
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

// githubUpload uploads or updates a file safely
func githubUpload(username, token, repo, branch, file, commitMsg string) error {
    pause(1)
    fmt.Printf("📄 Reading file: %s\n", file)
    content, err := ioutil.ReadFile(file)
    if err != nil {
        return fmt.Errorf("could not read file: %v", err)
    }

    pause(1)
    fmt.Println("🔑 Encoding content...")
    encoded := base64.StdEncoding.EncodeToString(content)

    url := fmt.Sprintf("https://api.github.com/repos/%s/%s/contents/%s?ref=%s", username, repo, file, branch)
    req, _ := http.NewRequest("GET", url, nil)
    req.SetBasicAuth(username, token)
    client := &http.Client{}
    resp, err := client.Do(req)
    var sha string
    if err == nil && resp.StatusCode == 200 {
        // File exists, get sha
        var result map[string]interface{}
        body, _ := ioutil.ReadAll(resp.Body)
        json.Unmarshal(body, &result)
        if s, ok := result["sha"].(string); ok {
            sha = s
        }
    }
    if resp != nil {
        resp.Body.Close()
    }

    // Use default commit message if blank
    if commitMsg == "" {
        commitMsg = "Update file"
    }

    payload := map[string]string{
        "message": commitMsg,
        "content": encoded,
        "branch":  branch,
    }
    if sha != "" {
        payload["sha"] = sha
    }

    data, _ := json.Marshal(payload)
    reqPut, _ := http.NewRequest("PUT",
        fmt.Sprintf("https://api.github.com/repos/%s/%s/contents/%s", username, repo, file),
        strings.NewReader(string(data)))
    reqPut.SetBasicAuth(username, token)
    reqPut.Header.Set("Accept", "application/vnd.github+json")

    pause(1)
    fmt.Println("🚀 Uploading file to GitHub...")
    respPut, err := client.Do(reqPut)
    if err != nil {
        return err
    }
    defer respPut.Body.Close()

    body, _ := ioutil.ReadAll(respPut.Body)
    if respPut.StatusCode >= 200 && respPut.StatusCode < 300 {
        fmt.Printf("✅ Upload successful: %s\n", file)
    } else {
        fmt.Printf("❌ Upload failed for %s:\n%s\n", file, string(body))
    }

    return nil
}

func main() {
    reader := bufio.NewReader(os.Stdin)

    fmt.Println("💻 Welcome to gogit – safe GitHub uploader")
    pause(1)

    fmt.Print("👤 GitHub username: ")
    username, _ := reader.ReadString('\n')
    username = strings.TrimSpace(username)

    fmt.Print("🔑 Personal Access Token: ")
    token, _ := reader.ReadString('\n')
    token = strings.TrimSpace(token)

    fmt.Print("📂 Repository name: ")
    repo, _ := reader.ReadString('\n')
    repo = strings.TrimSpace(repo)

    fmt.Print("🌿 Branch (main/master): ")
    branch, _ := reader.ReadString('\n')
    branch = strings.TrimSpace(branch)

    branchLower := strings.ToLower(branch)
    if branchLower != "main" && branchLower != "master" {
        branch = "main"
        fmt.Println("➡️ Invalid branch entered. Using default branch: main")
    }

    fmt.Print("📄 File(s) to upload (comma or space separated): ")
    fileInput, _ := reader.ReadString('\n')
    fileInput = strings.TrimSpace(fileInput)

    fmt.Print("✏️ Commit message (optional): ")
    commitMsg, _ := reader.ReadString('\n')
    commitMsg = strings.TrimSpace(commitMsg)

    pause(1)
    fmt.Println("\n⚡ Starting upload...")

    files := strings.FieldsFunc(fileInput, func(r rune) bool {
        return r == ',' || r == ' '
    })

    for _, file := range files {
        file = strings.TrimSpace(file)
        if file == "" {
            continue
        }
        err := githubUpload(username, token, repo, branch, file, commitMsg)
        if err != nil {
            fmt.Println("❌ Error:", err)
        }
    }

    fmt.Println("\n🎉 All files processed. Your files are now on GitHub!")
}
