import logging
import requests
import confidential_client
import msal
import atexit
import os.path
import json
from datetime import datetime

config = json.load(open("parameters.json"))

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

user_id = "users/81ac1f9a-b470-4af0-8018-2fd61644d6e9"
drive_id = "b!5ep1PXhxG0Km5Jqkf-u_DFufdhWHEjlHu4PtVKswFOR5Qfty_KoNSbRJUCcXIzx5"
bulletin_folder_id = "01STA2XAXZOOCEYHHI6FH2WGUNOAN6LYJU"

def get_access_token():
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

    logging.info(flow['message'])

    result = app.acquire_token_by_device_flow(flow)
    
  return result

def list_bulletin_folder(result):
    access_token =  result['access_token']
    list_bulletin_folder = f'{ENDPOINT}/{user_id}/drives/{drive_id}/items/{bulletin_folder_id}/children'
    result = requests.get(list_bulletin_folder, headers={'Authorization': 'Bearer ' + access_token})
    result.raise_for_status()
    json_data = result.json()
    return json_data

def get_bulletin_url():
  result = confidential_client.get_access_token(config)
  return get_url_to_latest_bulletin(result)

def get_url_to_latest_bulletin(result):
  if 'access_token' in result:
    json_data = list_bulletin_folder(result)
    access_token = result['access_token']
    most_recent = max(json_data["value"], key = lambda k: datetime.strptime(k["lastModifiedDateTime"], "%Y-%m-%dT%H:%M:%SZ"))

    share_link = f'{ENDPOINT}/{user_id}/drive/items/{most_recent["id"]}/createlink'
    anonymous_view={'type':'view', 'scope':'anonymous'}
    result = requests.post(share_link, headers={'Authorization': f'Bearer {access_token}'}, json=anonymous_view )
    result.raise_for_status()
    json_data = result.json()
    return result.json()["link"]["webUrl"]
    

  else:
    return "Nothing"
    #raise Exception('no access token in result')

def list_subs():
  result = get_access_token()
  if 'access_token' in result:
    access_token =  result['access_token']
    
    subscriptions = f'{ENDPOINT}/subscriptions'
    result = requests.get(subscriptions, headers={'Authorization': 'Bearer ' + access_token})
    result.raise_for_status()
    json_data = result.json()
    for sub_entry in json_data["value"]:
      logging.info(sub_entry["id"])

def show_login():

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

    return (flow['message'])

    result = app.acquire_token_by_device_flow(flow)
    
  return "nothing"

if __name__=="__main__":
      logging.info(get_bulletin_url())