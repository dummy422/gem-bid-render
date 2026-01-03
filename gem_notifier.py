import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime

TG_TOKEN = os.getenv("TG_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

if not TG_TOKEN or not CHAT_ID:
    raise Exception("Telegram credentials missing")

URL = "https://bidplus.gem.gov.in/bidlists"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

KEYWORDS = [
    "multi tier roller pot mill",
    "portable ball mill",
    "chemical vapour deposition",
    "hydraulic press",
    "high temperature vacuum hot press",
    "tubular furnace",
    "high temperature horizontal tube furnace",
    "sofc test bench",
    "bio mass pyrolysis",
    "vacuum hot press",
    "pot jar mill",
    "revamping of pot jar mill",
    "furnace",
    "hot press",
    "vacuum furnace",
    "pyrolysis reactor",
    "microwave casting furnace",
    "muffle furnace",
    "hot air oven",
    "ultrasonic spray pyrolysis",
    "stir casting furnace",
    "vacuum tubular furnace",
    "cvd system",
    "vertical dual zone furnace",
    "thyristor",
    "heating element",
    "hot corrosion tubular furnace",
    "gas sensing",
    "split tubular furnace",
    "raising hearth furnace",
    "vacuum compression moulding press",
    "compression assisted microwave furnace",
    "extruder",
    "homogenisation furnace",
    "hot pressing machine",
    "hmor tester",
    "table top horizontal single zone tube furnace",
    "vacuum annealing furnace",
    "lab value machine",
    "aluminium stir casting",
    "jar mill",
    "high temperature press",
    "microwave furnace",
    "magnesium stir casting"
]

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": message
    }, timeout=20)

response = requests.get(URL, headers=HEADERS, timeout=30)
soup = BeautifulSoup(response.text, "html.parser")

cards = soup.select(".card")
matches = []

for card in cards:
    text = card.get_text(" ", strip=True).lower()
    for kw in KEYWORDS:
        if kw in text:
            matches.append(f"🔔 {kw.upper()}\n{text[:350]}")
            break

if matches:
    send_telegram(
        f"🟢 GeM Bid Alert ({datetime.now().strftime('%d-%m-%Y %H:%M')})\n\n" +
        "\n\n".join(matches)
    )
else:
    send_telegram("✅ Render check OK. No matching GeM bids now.")
