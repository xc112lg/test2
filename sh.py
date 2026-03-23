import requests
import json

# load cookie json from text file
with open("cookie.txt", "r", encoding="utf-8") as f:
    cookie_json = json.load(f)

# convert to dict
cookies = {c["name"]: c["value"] for c in cookie_json}

# extract csrftoken
csrftoken = cookies.get("csrftoken", "")

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "accept": "application/json",
    "referer": "https://shopee.ph/user/voucher-wallet",
    "x-requested-with": "XMLHttpRequest",
    "x-csrftoken": csrftoken
}

url = "https://shopee.ph/api/v2/voucher_wallet/get_voucher_list"

params = {
    "voucher_status": 1,
    "limit": 100,
    "offset": 0
}

r = requests.get(url, headers=headers, cookies=cookies, params=params)

print("STATUS:", r.status_code)
print(r.text)
