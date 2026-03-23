import requests
import json

# load cookie json from text file
with open("cookie.txt", "r", encoding="utf-8") as f:
    cookies_json = json.loads(f.read())

# convert cookies
cookies = {c["name"]: c["value"] for c in cookies_json}

headers = {
    "user-agent": "Mozilla/5.0",
    "accept": "application/json",
    "referer": "https://shopee.ph/user/voucher-wallet",
    "x-requested-with": "XMLHttpRequest"
}

url = "https://shopee.ph/api/v4/voucher_wallet/get_vouchers"

params = {
    "voucher_status": 1
}

session = requests.Session()

r = session.get(
    url,
    headers=headers,
    cookies=cookies,
    params=params
)

data = r.json()

if "data" not in data:
    print("Request failed")
    print(data)
    exit()

vouchers = data["data"]["vouchers"]

print(f"\nFound {len(vouchers)} vouchers\n")

for v in vouchers:
    print("------")
    print("Name:", v.get("voucher_name"))
    print("Code:", v.get("voucher_code"))
    print("Min Spend:", v.get("min_spend"))
