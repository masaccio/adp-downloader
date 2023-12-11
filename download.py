import os
import sys
import requests
import json

SESSION_COOKIE = None
STATEMENTS_URL = (
    "https://my.adp.com/v1_0/O/A/payStatements?adjustments=yes&numberoflastpaydates=300"
)


def get_content(url):
    headers = {"Accept": "application/json, text/plain, */*"}
    cookies = {"SMSESSION": SESSION_COOKIE}
    r = requests.get(url, headers=headers, cookies=cookies)
    r.raise_for_status()
    return r.content


try:
    with open("cookies.txt", "r") as fh:
        SESSION_COOKIE = fh.read().strip()
except FileNotFoundError:
    print("cookies.txt: file not found", file=sys.stderr)
    sys.exit(1)


statement_data = get_content(STATEMENTS_URL)
if b"payStatements" not in statement_data:
    print("No statement data found: cookie has most likely expired", file=sys.stderr)
    sys.exit(1)

try:
    data = json.loads(statement_data)
except json.decoder.JSONDecodeError:
    print("Data is malformed JSON; giving up", file=sys.stderr)
    sys.exit(1)

for statement in data["payStatements"]:
    pay_date = str(statement["payDate"])
    (year, _, _) = pay_date.split("-")

    if os.path.exists(year) and not os.path.isdir(year):
        print(f"{year}: not a directory", file=sys.stderr)
        sys.exit(1)
    elif not os.path.exists(year):
        os.mkdir(year)

    if not os.path.exists(f"{year}/{pay_date}.json"):
        print(f"Saving {year}/{pay_date}")
        pay_data = get_content(
            "https://my.adp.com//" + str(statement["payDetailUri"]["href"])
        )
        with open(f"{year}/{pay_date}.json", "wb") as fh:
            fh.write(pay_data)

        pdf = get_content(
            "https://my.adp.com//" + str(statement["statementImageUri"]["href"])
        )
        with open(f"{year}/{pay_date}.pdf", "wb") as fh:
            fh.write(pdf)
