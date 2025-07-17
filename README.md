# ExtractHar

This is a Python script that extracts the contents of HAR files from Chromium based browsers (such as Edge, Chromium, Chrome, etc). This is useful for client-side web app analysis (SAST) and secret scanning.

---

## Features

- Extracts all contents
- Retains squence order
- Includes all headers, body, cookies and payloads including binaries

---

# Install
```
virtualenv venv
source ./venv/bin/activate
```

# Use
```
source ./venv/bin/activate
python extractHar.py yourSite.com.har
```
