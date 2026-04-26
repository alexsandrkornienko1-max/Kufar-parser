import requests, json, os, re, time
from datetime import datetime

SEARCH_URL = "https://re.kufar.by/l/minsk/kupit/kommercheskaya/magaziny?cmim=v.and%3A2&cur=USD&oph=1&st=r%3A0%2C50"   # вставь свою ссылку
TELEGRAM_BOT_TOKEN = "8517056028:AAHwxR1kXKaPBJYFqsljbXSQDM1y6yk7Ee0"
TELEGRAM_CHAT_ID = "5001350756"
KNOWN_IDS_FILE = "known_ids.json"

def get_ids():
    try:
        resp = requests.get(SEARCH_URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
        ids = re.findall(r'data-ad-id="(\d+)"', resp.text)
        if not ids:
            ids = re.findall(r'"ad_id":(\d+)', resp.text)
        return set(ids)
    except: return set()

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": text})

def main():
    print("Проверка...")
    current = get_ids()
    known = set(json.load(open(KNOWN_IDS_FILE))) if os.path.exists(KNOWN_IDS_FILE) else set()
    new = current - known
    for ad_id in new:
        send_telegram(f"🔔 Новое помещение!\nhttps://kufar.by/item/{ad_id}")
    with open(KNOWN_IDS_FILE, "w") as f: json.dump(list(known | current), f)

if __name__ == "__main__":
    main()