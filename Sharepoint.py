import requests
from msal import ConfidentialClientApplication
from urllib.parse import quote

TENANT_ID = "TENANT_ID"
CLIENT_ID = "CLIENT_ID"
CLIENT_SECRET = "CLIENT_SECRET"


SHAREPOINT_HOST = "shp"
SITE_PATH = quote("sites/site")
FOLDER_PATH = "sub/sub"


AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["https://graph.microsoft.com/.default"]

def get_token():
    app = ConfidentialClientApplication(
        CLIENT_ID,
        authority=AUTHORITY,
        client_credential=CLIENT_SECRET
    )
    result = app.acquire_token_for_client(scopes=SCOPES)

    if "access_token" not in result:
        raise Exception(result)

    return result["access_token"]

def get_json(url, token):
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(url, headers=headers, timeout=60, proxies=proxy)
    r.raise_for_status()
    return r.json()

def download_file(url, token, local_file):
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(url, headers=headers, timeout=300)
    r.raise_for_status()
    with open(local_file, "wb") as f:
        f.write(r.content)

token = get_token()
print(token)

# 1. Get site ID
site_url = f"https://graph.microsoft.com/v1.0/sites/{SHAREPOINT_HOST}:/{SITE_PATH}"
site = get_json(site_url, token)
site_id = site["id"]
print(site_id)

# 2. Get drives (document libraries)
drives_url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drives"
drives = get_json(drives_url, token)
print(drives)

# Usually first drive is Documents, but better inspect names
drive_id = drives["value"][0]["id"]

# 3. List files in folder
files_url = f"https://graph.microsoft.com/v1.0/drives/{drive_id}/root:/{FOLDER_PATH}:/children"
files = get_json(files_url, token)
print(files)

for item in files["value"]:
    if "file" in item:
        file_name = item["name"]
        item_id = item["id"]
        last_modified = item.get("lastModifiedDateTime")
        content_url = f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/{item_id}/content"
        print("Downloading:", file_name , ' last modified ', last_modified)
        if file_name == 'all_staff_data.csv':
            download_file(content_url, token, file_name)
