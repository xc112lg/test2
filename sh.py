import requests
import json

# load cookie json from text file
with open("cookie.txt", "r", encoding="utf-8") as f:
    cookies_json = json.loads(f.read())

# convert cookie json to dict
cookies = {c["name"]: c["value"] for c in cookies_json}

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "accept": "application/json",
    "referer": "https://shopee.ph/user/voucher-wallet",
    "x-requested-with": "XMLHttpRequest"
}

url = "https://shopee.ph/api/v2/voucher_wallet/vouchers"

params = {
    "voucher_status": 1,
    "limit": 100,
    "offset": 0
}

r = requests.get(url, headers=headers, cookies=cookies, params=params)

print("STATUS:", r.status_code)

data = r.json()
print(data)

if "data" not in data:
    print("No voucher data found")
    exit()

vouchers = data["data"].get("vouchers", [])

print(f"\nFound {len(vouchers)} vouchers\n")

for v in vouchers:
    print("------")
    print("Name:", v.get("voucher_name"))
    print("Code:", v.get("voucher_code"))
    print("Min Spend:", v.get("min_spend"))
