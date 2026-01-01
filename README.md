# 📧 ChatGPT Account Setup Assistant

A cross-platform Python script that helps you create ChatGPT accounts using temporary email addresses.

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows%20|%20Linux%20|%20macOS-lightgrey)
![License](https://img.shields.io/badge/License-MIT-green)
![Dependencies](https://img.shields.io/badge/Dependencies-None-brightgreen)

## ✨ Features

- � **Auto-generates** temporary email addresses
- 🔑 **Secure password** generation (16 chars with mixed case, numbers, symbols)
- 📬 **Inbox monitoring** — automatically detects verification emails
- 🌐 **Auto-opens browser** for signup and verification
- �🔄 **Auto-retry** with exponential backoff
- 🎨 **Colored terminal output** (cross-platform)
- � **Zero dependencies** — uses only Python standard library

## 🚀 Quick Start

### Prerequisites

- Python 3.8+ installed on your system

### Usage

```bash
python3 chatgpt.py
```

On Windows:

```bash
python chatgpt.py
```

## 📋 How It Works

The script guides you through 3 simple steps:

1. **Creates email & password** — Generates a temp email and secure password
2. **Opens ChatGPT signup** — Browser opens automatically; you complete signup
3. **Monitors inbox** — Automatically detects verification email and opens the link

At the end, you'll see your full login credentials to save.

## 📸 Example Output

```
╔══════════════════════════════════════════════════════════════╗
║        📧  ChatGPT Account Setup Assistant  📧               ║
╚══════════════════════════════════════════════════════════════╝

──────────────────────────────────────────────────────────────────
  Step 1: Creating Temporary Email
──────────────────────────────────────────────────────────────────

  ✔  Password generated: Kx9#mPqR2$vLnJ4w
  ✔  Email created: abcdefgh@erzi.me

╔══════════════════════════════════════════════════════════════╗
║              🎉  SETUP COMPLETE  🎉                          ║
╚══════════════════════════════════════════════════════════════╝

  � Email:    abcdefgh@erzi.me
  � Password: Kx9#mPqR2$vLnJ4w

  ⚠ Save these credentials! Account expires in 24 hours.
```

## ⚠️ Important Notes

> **Warning**: Generated accounts expire after **24 hours**.

- The script opens your default browser automatically
- Press `Ctrl+C` at any time to cancel
- Keep the terminal open while signing up

## 🔧 Troubleshooting

| Issue                      | Solution                                     |
| -------------------------- | -------------------------------------------- |
| `command not found`        | Ensure Python is installed and in your PATH  |
| `Connection errors`        | Check your internet connection               |
| `Rate limited`             | Wait a few minutes and try again             |
| `No verification email`    | Check the inbox link manually                |

## 📄 License

This project is licensed under the [MIT License](LICENSE).

> ⚠️ **Disclaimer**: This project is intended for **educational purposes only**. The author is not responsible for any misuse or violation of third-party Terms of Service. Use responsibly.
