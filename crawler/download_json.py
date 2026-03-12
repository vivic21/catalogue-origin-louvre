import os
import requests
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

BASE_URL = "https://collections.louvre.fr"

ARK_FILE = "../data/ark_ids.txt"
OUTPUT_DIR = "../data/raw/louvre_json"

MAX_THREADS = 60 #montable jusqu'à 150 avec SSD et proc solide


# créer dossier
os.makedirs(OUTPUT_DIR, exist_ok=True)


# session HTTP persistante
session = requests.Session()

retries = Retry(
    total=50,
    backoff_factor=1,
    status_forcelist=[500, 502, 503, 504]
)

adapter = HTTPAdapter(max_retries=retries)

session.mount("https://", adapter)
session.mount("http://", adapter)

# Download JSON

def download_one(ark):

    ark_id = ark.split("/")[-1] # cut ark:

    filepath = os.path.join(OUTPUT_DIR, ark_id + ".json")

    # skip si déjà téléchargé
    if os.path.exists(filepath):
        return

    url = BASE_URL + ark + ".json"

    try:

        r = session.get(url, timeout=60)

        if r.status_code == 200:

            with open(filepath, "w", encoding="utf8") as f:
                f.write(r.text)

    except Exception:
        pass


# chargement liste ARK
with open(ARK_FILE) as f:
    ark_ids = [line.strip() for line in f]


# téléchargement parallèle
with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:

    list(tqdm(executor.map(download_one, ark_ids), total=len(ark_ids)))

# warning 1 dossier de 500 000 fichier environ