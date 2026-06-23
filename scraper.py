from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup


HEADERS = {"User-Agent": "Mozilla/5.0"}

VENUE = "victoria-park"
COURTS = {168: "Court 1",
           169: "Court 2",
           171: "Court 3",
           172: "Court 4"}

TIMES = {"08:00", "09:00", "10:00", "17:00", "18:00", "19:00", "20:00", "21:00"}

def get_availability(date):

    url = f"https://tennistowerhamlets.com/book/courts/{VENUE}/{date}#book"

    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, 'html.parser')

    available = []

    for slot in soup.select("input.bookable"):

        venue_id, court_id, day, time = slot["value"].split("_")

        court_id = int(court_id)

        if court_id not in COURTS:
            continue

        if time not in TIMES:
            continue

        available.append({
            "date": day,
            "court": COURTS[court_id],
            "time": time
        })

    return available

all_available = []

for i in range(7):
    date = (datetime.today() + timedelta(days=i)).strftime("%Y-%m-%d")

    try:
        slots = get_availability(date)
        all_available.extend(slots)

    except Exception as e:
        print(f"Failed for {date}: {e}")


for slot in sorted(all_available, key=lambda x: (x['date'], x['time'])):
    print(f"{slot['date']} | {slot['court']} | {slot['time']}")
