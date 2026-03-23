import requests
import json
from datetime import datetime

# load cookie JSON from text file
with open("cookie.txt", "r", encoding="utf-8") as f:
    cookies_json = json.loads(f.read())

# convert cookies to string
cookie_string = "; ".join([f"{c['name']}={c['value']}" for c in cookies_json])

headers = {
    "cookie": cookie_string,
    "user-agent": "Mozilla/5.0",
    "accept": "application/json",
    "x-api-source": "pc",
    "referer": "https://shopee.ph/user/voucher-wallet"
}

url = "https://shopee.ph/api/v2/voucher_wallet/get_vouchers"

params = {
    "voucher_status": 1
}

r = requests.get(url, headers=headers)
data = r.json()

if "data" not in data:
    print("Failed to fetch vouchers")
    exit()

vouchers = data["data"]["vouchers"]

print(f"\nFound {len(vouchers)} vouchers\n")

for v in vouchers:
    name = v.get("voucher_name")
    code = v.get("voucher_code")
    discount = v.get("reward_value")
    min_spend = v.get("min_spend")
    end_time = v.get("end_time")

    if end_time:
        end_time = datetime.fromtimestamp(end_time).strftime("%Y-%m-%d %H:%M:%S")

    print("------")
    print("Name:", name)
    print("Code:", code)
    print("Discount:", discount)
    print("Min Spend:", min_spend)
    print("Expires:", end_time)
