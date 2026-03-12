import time
from bs4 import BeautifulSoup
from tqdm import tqdm

from crawler_utils import fetch

BASE_URL = "https://collections.louvre.fr"
SEARCH_URL = "https://collections.louvre.fr/recherche"

OUTPUT_FILE = "../data/ark_ids.txt"

# actuellement 502 000 oeuvres

MAX_PAGES = 120 # capacité 600 000 oeuvres

ark_ids = set()

for page in tqdm(range(1, MAX_PAGES)):

    url = f"{SEARCH_URL}?page={page}&limit=5000"   # accepte jusqu'à 10 000

    r = fetch(url)

    if not r:
        continue

    soup = BeautifulSoup(r.text, "html.parser")

    for link in soup.find_all("a"):

        href = link.get("href", "")

        if "/ark:/53355/" in href:

            ark = href.split("?")[0]

            ark_ids.add(ark)


with open(OUTPUT_FILE, "w") as f:

    for ark in sorted(ark_ids):
        f.write(ark + "\n")

print("ARK IDs found:", len(ark_ids))