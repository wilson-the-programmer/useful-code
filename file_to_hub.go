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

    payload := map[string]string{
        "message": commitMsg,
        "content": encoded,
        "branch":  branch,
    }
    data, _ := json.Marshal(payload)

    url := fmt.Sprintf("https://api.github.com/repos/%s/%s/contents/%s", username, repo, file)
    req, _ := http.NewRequest("PUT", url, strings.NewReader(string(data)))
    req.SetBasicAuth(username, token)
    req.Header.Set("Accept", "application/vnd.github+json")

    pause(1)
    fmt.Println("🚀 Uploading file to GitHub...")
    client := &http.Client{}
    resp, err := client.Do(req)
    if err != nil {
        return err
    }
    defer resp.Body.Close()

    body, _ := ioutil.ReadAll(resp.Body)

    if resp.StatusCode >= 200 && resp.StatusCode < 300 {
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

    fmt.Print("📄 File(s) to upload (comma or space separated): ")
    fileInput, _ := reader.ReadString('\n')
    fileInput = strings.TrimSpace(fileInput)

    fmt.Print("✏️ Commit message: ")
    commitMsg, _ := reader.ReadString('\n')
    commitMsg = strings.TrimSpace(commitMsg)

    pause(1)
    fmt.Println("\n⚡ Starting upload...")

    // Split input by commas or spaces
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
