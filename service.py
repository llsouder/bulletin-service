import requests
import msal
import atexit
import os.path
import json
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

def tooCool():
    return "too cool"

def getLatestBulletin():
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
    
  
    drive_id = "b!5ep1PXhxG0Km5Jqkf-u_DFufdhWHEjlHu4PtVKswFOR5Qfty_KoNSbRJUCcXIzx5"
    bulletin_folder_id = "01STA2XAXZOOCEYHHI6FH2WGUNOAN6LYJU"

    list_bulletin_folder = f'{ENDPOINT}/me/drives/{drive_id}/items/{bulletin_folder_id}/children'
    result = requests.get(list_bulletin_folder, headers={'Authorization': 'Bearer ' + access_token})
    result.raise_for_status()
    json_data = result.json()
    most_recent = max(json_data["value"], key = lambda k: datetime.strptime(k["lastModifiedDateTime"], "%Y-%m-%dT%H:%M:%SZ"))

    share_link = f'{ENDPOINT}/me/drive/items/{most_recent["id"]}/createlink'
    anonymous_view={'type':'view', 'scope':'anonymous'}
    result = requests.post(share_link, headers={'Authorization': f'Bearer {access_token}'}, json=anonymous_view )
    result.raise_for_status()
    json_data = result.json()
    return result.json()["link"]["webUrl"]
    

  else:
    raise Exception('no access token in result')

if __name__=="__main__":
      getLatestBulletin()