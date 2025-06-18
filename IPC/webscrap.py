import requests
from bs4 import BeautifulSoup
import json

url = "https://www.sci.gov.in/landmark-judgment-summaries/?judgment_year=2024"
headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, "html.parser")

judgments = []

# Find the table
table = soup.find("table")
if table:
    rows = table.find_all("tr")[1:]  # skip header
    for row in rows:
        cells = row.find_all("td")
        if len(cells) >= 5:
            judgments.append({
                "serial_number": cells[0].get_text(strip=True),
                "date_of_judgment": cells[1].get_text(strip=True),
                "cause_title": cells[2].get_text(strip=True),
                "subject": cells[3].get_text(strip=True),
                "summary": cells[4].get_text(strip=True)
            })

# Save to JSON file
import os
print("Saving to:", os.getcwd())
with open("landmark_judgments_2024.json", "w", encoding="utf-8") as f:
    json.dump(judgments, f, indent=2, ensure_ascii=False)

print(f"✅ Successfully scraped {len(judgments)} landmark judgments for 2024.")
