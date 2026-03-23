import requests
import json
from datetime import datetime

# load cookie json from text file
with open("cookie.txt", "r", encoding="utf-8") as f:
    cookie_json = json.load(f)

# convert to dict
cookies = {c["name"]: c["value"] for c in cookie_json}

headers = {
    "user-agent": "Mozilla/5.0",
    "accept": "application/json",
    "referer": "https://shopee.ph/user/voucher-wallet",
    "x-requested-with": "XMLHttpRequest"
}

url = "https://shopee.ph/api/v2/voucher_wallet/get_voucher_list"

params = {
    "voucher_status": 1,
    "offset": 0,
    "limit": 100
}

r = requests.get(url, headers=headers, cookies=cookies, params=params)

print("Status:", r.status_code)

data = r.json()

if "data" not in data:
    print("API response:")
    print(data)
    exit()

vouchers = data["data"].get("vouchers", [])

print(f"\nFound {len(vouchers)} vouchers\n")

for v in vouchers:
    name = v.get("voucher_name")
    code = v.get("voucher_code")
    min_spend = v.get("min_spend")
    end = v.get("end_time")

    if end:
        end = datetime.fromtimestamp(end).strftime("%Y-%m-%d %H:%M:%S")

    print("------")
    print("Name:", name)
    print("Code:", code)
    print("Min Spend:", min_spend)
    print("Expires:", end)
