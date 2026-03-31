import requests
import json
import time
import random
from datetime import datetime, timezone

DATA_FILE = "cars.json"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "ko-KR,ko;q=0.9",
    "Referer": "https://www.encar.com/",
    "Origin": "https://www.encar.com",
}

BASE_URL = "https://api.encar.com/search/car/list/general"

MANUFACTURER_MAP = {
    "현대": "Hyundai", "기아": "Kia", "제네시스": "Genesis",
    "쉐보레(GM대우)": "Chevrolet", "르노코리아(삼성)": "Renault Korea",
    "KG모빌리티(쌍용)": "KG Mobility", "벤츠": "Mercedes-Benz",
    "BMW": "BMW", "아우디": "Audi", "폭스바겐": "Volkswagen",
    "볼보": "Volvo", "포르쉐": "Porsche", "렉서스": "Lexus",
    "토요타": "Toyota", "혼다": "Honda", "닛산": "Nissan",
    "랜드로버": "Land Rover", "재규어": "Jaguar", "벤틀리": "Bentley",
    "페라리": "Ferrari", "람보르기니": "Lamborghini", "마세라티": "Maserati",
    "미니": "MINI", "푸조": "Peugeot", "시트로엥": "Citroën",
    "링컨": "Lincoln", "캐딜락": "Cadillac", "지프": "Jeep",
    "포드": "Ford", "테슬라": "Tesla", "인피니티": "Infiniti",
}

# CarType.A = Korean domestic, CarType.Y = imported
QUERIES = ["(And.CarType.A.)", "(And.CarType.Y.)"]


def fetch_with_retry(url, params, retries=3, backoff=2):
    for attempt in range(retries):
        try:
            resp = requests.get(url, params=params, headers=HEADERS, timeout=15)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(backoff * (attempt + 1))
            else:
                print(f"[ERROR] {e}")
    return None


def fetch_cars(total=40):
    cars = []
    per_query = total // len(QUERIES)  # 20 each

    for q in QUERIES:
        start = 0
        collected = 0

        while collected < per_query:
            batch = min(20, per_query - collected)
            data = fetch_with_retry(BASE_URL, {
                "q": q,
                "sr": f"|ModifiedDate|{start}|{batch}",
                "count": "true",
            })
            if not data:
                break

            items = data.get("SearchResults", [])
            if not items:
                break

            for item in items:
                car = parse_car(item)
                if car:
                    cars.append(car)
                    collected += 1
                    if collected >= per_query:
                        break

            if len(items) < batch:
                break

            start += batch
            time.sleep(random.uniform(0.5, 1.0))

    return cars[:total]


def parse_car(item):
    try:
        car_id = item.get("Id", "")
        manufacturer = item.get("Manufacturer", "")
        model = item.get("Model", "")
        badge = item.get("Badge", "")
        year = item.get("Year", "")
        mileage = item.get("Mileage", 0)
        price = item.get("Price", 0)

        photo = ""
        photos = item.get("Photos", [])
        if photos:
            loc = photos[0].get("location", "")
            if loc:
                photo = f"https://ci.encar.com{loc}"

        manufacturer_en = MANUFACTURER_MAP.get(manufacturer, manufacturer)
        name = f"{manufacturer_en} {model}"
        if badge:
            name += f" {badge}"

        return {
            "id": car_id,
            "name": name.strip(),
            "manufacturer": manufacturer_en,
            "model": model,
            "year": year,
            "mileage": mileage,
            "price": price,
            "photo": photo,
            "url": f"https://www.encar.com/dc/dc_cardetailview.do?carid={car_id}",
        }
    except Exception as e:
        print(f"[WARN] parse_car: {e}")
        return None


def save(cars):
    payload = {
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "count": len(cars),
        "cars": cars,
    }
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    print(f"[OK] Saved {len(cars)} cars → {DATA_FILE}")


def run():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Parsing encar.com...")
    cars = fetch_cars(40)
    if cars:
        save(cars)
    else:
        print("[WARN] No cars fetched.")


if __name__ == "__main__":
    run()
