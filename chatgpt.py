import requests
import random
import string
import time

URL = "https://temp-mail.lu-la.workers.dev/api/new_address"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/json"
}


def random_name(length=8):
    """Generate random lowercase name"""
    return "".join(random.choice(string.ascii_lowercase) for _ in range(length))


def create_address():
    while True:
        name = random_name()
        payload = {
            "name": name,
            "domain": "erzi.me",
            "cf_token": ""
        }

        try:
            resp = requests.post(URL, headers=HEADERS, json=payload, timeout=15)
            print(f"Trying name: {name} — Status: {resp.status_code}")

            # If status is not 200 → retry
            if resp.status_code != 200:
                print("Not 200 — retrying...")
                time.sleep(1)
                continue

            body = resp.text.strip()

            # Empty response
            if not body:
                print("Empty response — retrying...")
                time.sleep(1)
                continue

            # Cloudflare / HTML page instead of JSON
            if "<html" in body.lower() or "cloudflare" in body.lower():
                print("Non-API page returned — retrying...")
                time.sleep(2)
                continue

            # Safe JSON parse
            data = resp.json()

            jwt = data.get("jwt")
            if not jwt:
                print("No JWT in response — retrying...")
                time.sleep(1)
                continue

            link = f"https://em.bjedu.tech/?jwt={jwt}"

            print("\nSUCCESS")
            print("Email:", data.get("address"))
            print("Link:", link)
            return

        except Exception as e:
            print("Error:", e)
            time.sleep(1)


if __name__ == "__main__":
    create_address()
