import requests
import msal
import atexit
import os.path
from datetime import datetime

TENANT_ID = '356e67d4-d13d-44fe-815b-3fb842925be4'
CLIENT_ID = '208496d8-671c-4f89-8df6-ceded22c8a2e'
SHAREPOINT_HOST_NAME = 'victorybible.sharepoint.com'

AUTHORITY = 'https://login.microsoftonline.com/' + TENANT_ID
ENDPOINT = 'https://graph.microsoft.com/v1.0'

SCOPES = [
    'Files.ReadWrite.All',
    'Sites.ReadWrite.All',
    'User.Read',
    'User.ReadBasic.All'
]

cache = msal.SerializableTokenCache()

if os.path.exists('token_cache.bin'):
    cache.deserialize(open('token_cache.bin', 'r').read())

atexit.register(lambda: open('token_cache.bin', 'w').write(cache.serialize()) if cache.has_state_changed else None)

app = msal.PublicClientApplication(CLIENT_ID, authority=AUTHORITY, token_cache=cache)

accounts = app.get_accounts()
result = None
if len(accounts) > 0:
    result = app.acquire_token_silent(SCOPES, account=accounts[0])

if result is None:
    flow = app.initiate_device_flow(scopes=SCOPES)
    if 'user_code' not in flow:
        raise Exception('Failed to create device flow')

    print(flow['message'])

    result = app.acquire_token_by_device_flow(flow)

if 'access_token' in result:
    access_token =  result['access_token']
    # onedrive = 'me'
    # result = requests.get(f'{ENDPOINT}/{onedrive}', headers={'Authorization': 'Bearer ' + access_token})
    # result.raise_for_status()
    # print(result.json())
    

    onedrive = "me/drives/b!5ep1PXhxG0Km5Jqkf-u_DFufdhWHEjlHu4PtVKswFOR5Qfty_KoNSbRJUCcXIzx5/items/01STA2XAXZOOCEYHHI6FH2WGUNOAN6LYJU/children"
    result = requests.get(f'{ENDPOINT}/{onedrive}', headers={'Authorization': 'Bearer ' + access_token})
    result.raise_for_status()
    json_data = result.json()
    for value in json_data["value"] :
        print(value["name"])
    oldest = max(json_data["value"], key = lambda k: datetime.strptime(k["lastModifiedDateTime"], "%Y-%m-%dT%H:%M:%SZ"))
    # "lastModifiedDateTime": "2021-03-18T03:20:57Z"
    print(f'This is so new {oldest["name"]}')
    print(f'This is so new {oldest["webUrl"]}')
   
    

else:
    raise Exception('no access token in result')