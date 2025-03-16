import requests

# vManage Sandbox Details
VMANAGE_HOST = "https://sandbox-sdwan-2.cisco.com"
USERNAME = "devnetuser"
PASSWORD = "RG!_Yw919_83"

# Disable SSL warnings (for testing)
requests.packages.urllib3.disable_warnings()

def authenticate():
    """Authenticate to Cisco vManage and return JSESSIONID"""
    url = f"{VMANAGE_HOST}/j_security_check"
    payload = {"j_username": USERNAME, "j_password": PASSWORD}

    session = requests.session()
    response = session.post(url, data=payload, verify=False)

    if response.status_code == 200 and "Set-Cookie" in response.headers:
        print("[✔] Authentication Successful!")
        return session  # Returning the session with cookies stored
    else:
        print("[✖] Authentication Failed!")
        return None

def get_devices(session):
    """Fetch list of devices from vManage API"""
    url = f"{VMANAGE_HOST}/dataservice/device"
    response = session.get(url, verify=False)

    if response.status_code == 200:
        devices = response.json()['data']
        print("\n[✔] Retrieved Device List:")
        for device in devices:
            print(f"- {device['host-name']} ({device['device-type']}) - {device['system-ip']}")
    else:
        print("[✖] Failed to fetch devices!")

# Run the script
session = authenticate()
if session:
    get_devices(session)
