import csv
from datetime import datetime
import requests

# Target endpoint for public market/crypto data
API_URL = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd&include_24hr_change=true"
OUTPUT_FILE = "market_data_log.csv"


def fetch_data():
    """Fetch real-time data from the target API endpoint."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AutomationScript/1.0"
    }
    try:
        response = requests.get(API_URL, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Extraction failed: {e}")
        return None


def process_and_save(data):
    """Process incoming JSON payload and append formatted rows to CSV."""
    if not data:
        return

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Determine if file exists to control header writing
    file_exists = False
    try:
        with open(OUTPUT_FILE, "r"):
            file_exists = True
    except FileNotFoundError:
        pass

    with open(OUTPUT_FILE, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(["Timestamp", "Asset", "Price USD", "24h Change %"])

        for asset, metrics in data.items():
            price = metrics.get("usd", 0)
            change = round(metrics.get("usd_24h_change", 0), 2)
            writer.writerow(
                [timestamp, asset.upper(), f"${price}", f"{change}%"]
            )

    print(f"[{timestamp}] Successfully updated {OUTPUT_FILE}")


def run_pipeline():
    print("Starting Automated Data Extractor Pipeline...")
    data = fetch_data()
    process_and_save(data)


if __name__ == "__main__":
    run_pipeline()
