# 📧 Temporary Email Generator for ChatGPT Teachers

A cross-platform Python script that generates temporary email addresses for ChatGPT Teachers verification.

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows%20|%20Linux%20|%20macOS-lightgrey)
![License](https://img.shields.io/badge/License-MIT-green)

## ✨ Features

- 🔄 **Auto-retry** with exponential backoff
- 🎨 **Colored terminal output** (cross-platform)
- 🛡️ **Robust error handling** for network issues
- 🖥️ **Works on** Windows, Linux, and macOS

## 🚀 Quick Start

### Prerequisites

- Python installed on your system

### Usage

```bash
python3 chatgpt.py
```

On Windows, you can also use:

```bash
python chatgpt.py
```

## 📋 How It Works

1. **Run the script** — It generates a random temporary email address
2. **Copy the link** — Open it in a **private/incognito browser window**
3. **Verify on ChatGPT** — Go to [ChatGPT for Teachers](https://chatgpt.com/k12-verification) and sign in with the generated email
4. **Check inbox** — Return to the temp mail page to view verification emails

## 📸 Example Output

```
╔══════════════════════════════════════════════════════════════╗
║           📧  Temporary Email Generator  📧                  ║
╚══════════════════════════════════════════════════════════════╝

  ℹ  Starting email generation...

  →  Attempt 1/30: Trying 'abcdefgh@erzi.me'

╔══════════════════════════════════════════════════════════════╗
║                    ✅  SUCCESS  ✅                           ║
╚══════════════════════════════════════════════════════════════╝

  📬 Email:  abcdefgh@erzi.me
  🔗 Link:   https://em.bjedu.tech/en?jwt=...
```

## ⚠️ Important Notes

> **Warning**: Generated accounts expire after **24 hours**. Run the script again to create a new one.

- Always use a **private/incognito window** when opening the link
- The script automatically retries on network errors
- Press `Ctrl+C` to cancel at any time

## 🔧 Troubleshooting

| Issue               | Solution                                    |
| ------------------- | ------------------------------------------- |
| `command not found` | Ensure Python is installed and in your PATH |
| `Connection errors` | Check your internet connection              |
| `Rate limited`      | Wait a few minutes and try again            |

## 📄 License

This project is licensed under the [MIT License](LICENSE).

> ⚠️ **Disclaimer**: This project is intended for **educational purposes only**. The author is not responsible for any misuse or violation of third-party Terms of Service. Use responsibly.
