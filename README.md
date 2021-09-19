# adp-downloader

A more [featured Ruby version exists](https://github.com/andersonvom/adp-downloader) for downloading ADP payslips but Ruby appears terminally broken on Arm architecture Macs, so this is a simple Python version.

## Requirements

No username or password is required, but you must copy the session cookie from an active login session in your browser. ADP require Javascript to run through the login process and it also seems to resist scriping with Selenium.

Copy the contents of the `SMSESSION` cookie from your browser session and place in a file called `cookies.txt` in the current directoy.

## Usage

The downloader downloads all available payslips (there is a built-in limit in the script of 300) that do not exist locally. Invocation is simply:

```
python3 download.py
```

A folder will be created in the current working directory for each year and both JSON data as well as a PDF copy of the payslip is downloaded into these folders.
