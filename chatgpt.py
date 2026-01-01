#!/usr/bin/env python3
"""
ChatGPT Account Setup Assistant
Creates temporary email addresses with password generation for ChatGPT signup.
Cross-platform compatible (Linux, Windows, macOS).
Zero external dependencies - uses only Python standard library.
"""

import json
import random
import string
import time
import sys
import os
import ssl
import socket
import webbrowser
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

# ─────────────────────────────────────────────────────────────────────────────
# Cross-platform color support
# ─────────────────────────────────────────────────────────────────────────────

def _enable_windows_ansi():
    """Enable ANSI escape code support on Windows 10+."""
    if sys.platform == "win32":
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
        except Exception:
            pass

_enable_windows_ansi()


class Colors:
    """ANSI color codes for terminal output."""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    
    @classmethod
    def disable(cls):
        """Disable colors (for non-TTY or unsupported terminals)."""
        for attr in dir(cls):
            if not attr.startswith('_') and attr.isupper():
                setattr(cls, attr, "")


# Disable colors if not a TTY or if NO_COLOR env var is set
if not sys.stdout.isatty() or os.environ.get("NO_COLOR"):
    Colors.disable()


# ─────────────────────────────────────────────────────────────────────────────
# UI Components
# ─────────────────────────────────────────────────────────────────────────────

def print_banner():
    """Display the application banner."""
    banner = f"""
{Colors.CYAN}{Colors.BOLD}╔══════════════════════════════════════════════════════════════╗
║        📧  ChatGPT Account Setup Assistant  📧               ║
╚══════════════════════════════════════════════════════════════╝{Colors.RESET}
"""
    print(banner)


def print_status(message: str, status: str = "info"):
    """Print a formatted status message."""
    icons = {
        "info": f"{Colors.BLUE}ℹ{Colors.RESET}",
        "success": f"{Colors.GREEN}✔{Colors.RESET}",
        "warning": f"{Colors.YELLOW}⚠{Colors.RESET}",
        "error": f"{Colors.RED}✖{Colors.RESET}",
        "retry": f"{Colors.YELLOW}↻{Colors.RESET}",
        "attempt": f"{Colors.MAGENTA}→{Colors.RESET}",
    }
    icon = icons.get(status, icons["info"])
    print(f"  {icon}  {message}")


def print_credentials_box(email: str, password: str, inbox_link: str):
    """Print the credentials in a formatted box."""
    print()
    print(f"{Colors.GREEN}{Colors.BOLD}╔══════════════════════════════════════════════════════════════╗")
    print(f"║                    ✅  SUCCESS  ✅                           ║")
    print(f"╚══════════════════════════════════════════════════════════════╝{Colors.RESET}")
    print()
    print(f"  {Colors.BOLD}Your Credentials:{Colors.RESET}")
    print()
    print(f"  {Colors.BOLD}📧 Email:{Colors.RESET}    {Colors.CYAN}{email}{Colors.RESET}")
    print(f"  {Colors.BOLD}🔑 Password:{Colors.RESET} {Colors.YELLOW}{password}{Colors.RESET}")
    print()
    print(f"  {Colors.BOLD}📬 Inbox:{Colors.RESET}    {Colors.BLUE}{inbox_link}{Colors.RESET}")
    print()
    print(f"  {Colors.BOLD}{Colors.YELLOW}⚠ Save these credentials! Account expires in 24 hours.{Colors.RESET}")
    print()


def print_instructions():
    """Print signup instructions."""
    print()
    print(f"  {Colors.BOLD}Next Steps:{Colors.RESET}")
    print(f"  {Colors.DIM}1.{Colors.RESET} Open the inbox link above in a {Colors.BOLD}private/incognito{Colors.RESET} window")
    print(f"  {Colors.DIM}2.{Colors.RESET} Go to {Colors.CYAN}https://chatgpt.com/k12-verification{Colors.RESET}")
    print(f"  {Colors.DIM}3.{Colors.RESET} Sign up using the email and password above")
    print(f"  {Colors.DIM}4.{Colors.RESET} Check the inbox for the verification email")
    print()


def print_error_box(title: str, message: str):
    """Print an error message in a formatted box."""
    print()
    print(f"{Colors.RED}{Colors.BOLD}╔══════════════════════════════════════════════════════════════╗")
    print(f"║  ❌  {title:<56} ║")
    print(f"╚══════════════════════════════════════════════════════════════╝{Colors.RESET}")
    print(f"  {Colors.DIM}{message}{Colors.RESET}")
    print()


# ─────────────────────────────────────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────────────────────────────────────

API_URL = "https://temp-mail.lu-la.workers.dev/api/new_address"
DEFAULT_DOMAIN = "erzi.me"
MAX_RETRIES = 30
BASE_DELAY = 1.0  # seconds
MAX_DELAY = 10.0  # seconds
REQUEST_TIMEOUT = 15  # seconds

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/json"
}


# ─────────────────────────────────────────────────────────────────────────────
# Core Functions
# ─────────────────────────────────────────────────────────────────────────────

def random_name(length: int = 8) -> str:
    """Generate a random lowercase name."""
    return "".join(random.choice(string.ascii_lowercase) for _ in range(length))


def generate_password(length: int = 16) -> str:
    """Generate a secure random password."""
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    special = "!@#$%&*"
    
    # Guarantee at least one of each type
    password = [
        random.choice(lowercase),
        random.choice(uppercase),
        random.choice(digits),
        random.choice(special),
    ]
    
    # Fill the rest with random characters
    all_chars = lowercase + uppercase + digits + special
    password.extend(random.choice(all_chars) for _ in range(length - 4))
    
    # Shuffle to randomize position
    random.shuffle(password)
    return "".join(password)


def calculate_backoff(attempt: int) -> float:
    """Calculate exponential backoff delay with jitter."""
    delay = min(BASE_DELAY * (2 ** attempt), MAX_DELAY)
    jitter = delay * 0.25 * (random.random() * 2 - 1)
    return delay + jitter


def make_request(url: str, payload: dict) -> tuple[int, str]:
    """Make an HTTP POST request."""
    data = json.dumps(payload).encode("utf-8")
    request = Request(url, data=data, headers=HEADERS, method="POST")
    context = ssl.create_default_context()
    
    try:
        with urlopen(request, timeout=REQUEST_TIMEOUT, context=context) as response:
            return response.status, response.read().decode("utf-8")
    except HTTPError as e:
        return e.code, e.read().decode("utf-8") if e.fp else ""


def create_address() -> dict | None:
    """
    Attempt to create a temporary email address.
    
    Returns:
        dict with 'email', 'link', and 'jwt' on success, None on failure.
    """
    for attempt in range(MAX_RETRIES):
        name = random_name()
        payload = {
            "name": name,
            "domain": DEFAULT_DOMAIN,
            "cf_token": ""
        }
        
        attempt_msg = f"Attempt {attempt + 1}/{MAX_RETRIES}: Trying '{Colors.CYAN}{name}@{DEFAULT_DOMAIN}{Colors.RESET}'"
        print_status(attempt_msg, "attempt")
        
        try:
            status_code, body = make_request(API_URL, payload)
            
            if status_code == 429:
                print_status("Rate limited (429) — backing off...", "warning")
                time.sleep(calculate_backoff(attempt))
                continue
            
            if status_code >= 500:
                print_status(f"Server error ({status_code}) — retrying...", "warning")
                time.sleep(calculate_backoff(attempt))
                continue
            
            if status_code != 200:
                print_status(f"Unexpected status ({status_code}) — retrying...", "warning")
                time.sleep(BASE_DELAY)
                continue
            
            body = body.strip()
            if not body:
                print_status("Empty response — retrying...", "retry")
                time.sleep(BASE_DELAY)
                continue
            
            if "<html" in body.lower() or "cloudflare" in body.lower():
                print_status("Cloudflare challenge detected — backing off...", "warning")
                time.sleep(calculate_backoff(attempt))
                continue
            
            try:
                data = json.loads(body)
            except json.JSONDecodeError:
                print_status("Invalid JSON response — retrying...", "warning")
                time.sleep(BASE_DELAY)
                continue
            
            jwt = data.get("jwt")
            if not jwt:
                print_status("No JWT in response — retrying...", "retry")
                time.sleep(BASE_DELAY)
                continue
            
            email = data.get("address", f"{name}@{DEFAULT_DOMAIN}")
            link = f"https://em.bjedu.tech/en?jwt={jwt}"
            
            return {"email": email, "link": link, "jwt": jwt}
        
        except socket.timeout:
            print_status("Request timed out — retrying...", "warning")
            time.sleep(calculate_backoff(attempt))
        
        except URLError as e:
            if isinstance(e.reason, socket.timeout):
                print_status("Connection timed out — retrying...", "warning")
            elif isinstance(e.reason, ssl.SSLError):
                print_status("SSL certificate error — retrying...", "error")
            else:
                print_status(f"Connection failed: {e.reason}", "error")
            time.sleep(calculate_backoff(attempt))
        
        except OSError as e:
            print_status(f"Network error: {e}", "error")
            time.sleep(calculate_backoff(attempt))
    
    return None


def open_url(url: str) -> bool:
    """Open URL in default browser."""
    try:
        webbrowser.open(url)
        return True
    except Exception:
        return False


def main():
    """Main entry point."""
    print_banner()
    
    # Generate password first
    print_status("Generating secure password...", "info")
    password = generate_password(16)
    print_status(f"Password generated: {Colors.YELLOW}{password}{Colors.RESET}", "success")
    print()
    
    # Create email
    print_status("Creating temporary email address...", "info")
    
    try:
        result = create_address()
        
        if not result:
            print_error_box(
                "Email Creation Failed",
                f"Failed to create email after {MAX_RETRIES} attempts. Please try again."
            )
            return 1
        
        email = result["email"]
        inbox_link = result["link"]
        
        # Show credentials
        print_credentials_box(email, password, inbox_link)
        
        # Show instructions
        print_instructions()
        
        # Ask if user wants to open browser
        print(f"  {Colors.BOLD}Open inbox in browser? [Y/n]:{Colors.RESET} ", end="")
        try:
            response = input().strip().lower()
            if response != 'n':
                if open_url(inbox_link):
                    print_status("Inbox opened in browser", "success")
                else:
                    print_status("Could not open browser automatically", "warning")
        except EOFError:
            pass
        
        print()
        return 0
    
    except KeyboardInterrupt:
        print()
        print_status("Operation cancelled by user.", "warning")
        return 130


if __name__ == "__main__":
    sys.exit(main())
