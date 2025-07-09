import requests
import sys
import os
import json

# Add project root to path to allow imports from other directories
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.database import SessionLocal, engine, Base
from database.models import Outlet
from sqlalchemy.orm import Session

API_URL = "https://www.mcdonalds.com.my/storefinder/index.php"

PAYLOAD = {
    "ajax": "1",
    "action": "get_nearby_stores",
    "distance": "10000",
    "lat": "",
    "lng": "",
    "state": "Kuala Lumpur",
    "products": "",
    "address": "Kuala Lumpur, Malaysia",
    "issuggestion": "0",
    "islocateus": "0"
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
}

def scrape_outlets():
    # Ensure the database and tables are created before scraping
    Base.metadata.create_all(bind=engine)

    db: Session = SessionLocal()

    try:
        print("Scraping McDonald's outlets in Kuala Lumpur...")
        response = requests.post(API_URL, data=PAYLOAD, headers=HEADERS)
        response.raise_for_status() # Raise an exception for bad status codes
        
        # Manually remove BOM if present and parse JSON
        cleaned_text = response.text.lstrip('\ufeff')
        data = json.loads(cleaned_text)

        if not data.get("success") or "stores" not in data:
            print("Error: Could not find 'stores' in the response.")
            return

        outlets = data.get('stores', [])
        if not outlets:
            print("No outlets found.")
            return

        for item in outlets:
            # Join all category names to form the operating_hours string
            operating_hours = ', '.join([c['cat_name'] for c in item.get('cat', [])])
            waze_link = f"https://waze.com/ul?ll={item['lat']},{item['lng']}&navigate=yes"

            # Check if outlet already exists
            existing_outlet = db.query(Outlet).filter(Outlet.name == item['name']).first()
            if existing_outlet:
                print(f"Outlet '{item['name']}' already exists. Updating.")
                existing_outlet.address = item['address']
                existing_outlet.operating_hours = operating_hours
                existing_outlet.waze_link = waze_link
                existing_outlet.latitude = float(item['lat'])
                existing_outlet.longitude = float(item['lng'])
            else:
                print(f"Adding new outlet: '{item['name']}'.")
                new_outlet = Outlet(
                    name=item['name'],
                    address=item['address'],
                    operating_hours=operating_hours,
                    waze_link=waze_link,
                    latitude=float(item['lat']),
                    longitude=float(item['lng'])
                )
                db.add(new_outlet)


        
        db.commit()
        print(f"Successfully scraped and saved {len(outlets)} outlets.")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the request: {e}")
        db.rollback()
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON: {e}")
        print("Raw response text:", response.text[:500]) # Print first 500 chars for debugging
        db.rollback()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    scrape_outlets()
    print("Scraping complete.")
