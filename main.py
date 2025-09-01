from flask import Flask, request
import os
import requests
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import pytz
from dotenv import load_dotenv
from cuelinks_fetcher import fetch_deals

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

app = Flask(__name__)
scheduler = BackgroundScheduler(timezone=pytz.timezone("Asia/Kolkata"))

TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

def send_deal(deal):
    if deal["image"]:
        url = f"{TELEGRAM_API}/sendPhoto"
        payload = {
            "chat_id": CHANNEL_ID,
            "photo": deal["image"],
            "caption": f"🔥 {deal['title']}\n👉 {deal['link']}"
        }
    else:
        url = f"{TELEGRAM_API}/sendMessage"
        payload = {
            "chat_id": CHANNEL_ID,
            "text": f"🔥 {deal['title']}\n👉 {deal['link']}"
        }
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print("Error sending deal:", e)

def post_scheduled_deals():
    print("Posting scheduled deals at", datetime.now())
    categories = ["shopping", "grocery", "food", "recharge", "ride", "insurance", "medicine", "travel"]
    for category in categories:
        deals = fetch_deals(limit=1)  # ek category ka ek deal
        for deal in deals:
            send_deal(deal)

# Scheduler timings (6, 9, 12, 15, 18 hours IST)
for hour in [6, 9, 12, 15, 18]:
    scheduler.add_job(post_scheduled_deals, "cron", hour=hour, minute=0)

scheduler.start()

@app.route("/")
def home():
    return "Deal Bot Running!"

@app.route("/setwebhook")
def set_webhook():
    webhook_url = request.url_root + "webhook"
    url = f"{TELEGRAM_API}/setWebhook?url={webhook_url}"
    res = requests.get(url).json()
    return res

@app.route("/webhook", methods=["POST"])
def webhook():
    return {"ok": True}
