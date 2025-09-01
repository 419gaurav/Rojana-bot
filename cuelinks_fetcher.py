import requests
import random
import os

API_KEY = os.getenv("CUELINKS_API_KEY")
PUBLISHER_ID = os.getenv("CUELINKS_PUBLISHER_ID")

def fetch_deals(category=None, limit=5):
    url = f"https://api.cuelinks.com/v2/offers?limit={limit}&publisher_id={PUBLISHER_ID}"
    headers = {"Authorization": f"Token {API_KEY}"}
    
    try:
        res = requests.get(url, headers=headers)
        res.raise_for_status()
        data = res.json()
        offers = data.get("offers", [])

        # shuffle deals
        random.shuffle(offers)

        deals = []
        for offer in offers[:limit]:
            deals.append({
                "title": offer.get("title", "Best Deal"),
                "link": offer.get("tracking_url", "#"),
                "image": offer.get("image", None)
            })
        return deals
    except Exception as e:
        print("Error fetching deals:", e)
        return []
