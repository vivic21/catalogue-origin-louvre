import requests
import time

HEADERS = {
    "User-Agent": "catalogue-origin-louvre-research-bot"
}

def fetch(url, retries=30):

    for _ in range(retries):

        try:
            r = requests.get(url, headers=HEADERS, timeout=15)

            if r.status_code == 200:
                return r

        except:
            pass

        time.sleep(0.1)

    return None