import requests
import msal

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

app = msal.PublicClientApplication(CLIENT_ID, authority=AUTHORITY)

flow = app.initiate_device_flow(scopes=SCOPES)
if 'user_code' not in flow:
    raise Exception('Failed to create device flow')

print(flow['message'])

result = app.acquire_token_by_device_flow(flow)

if 'access_token' in result:
    result = requests.get(f'{ENDPOINT}/me', headers={'Authorization': 'Bearer ' + result['access_token']})
    result.raise_for_status()
    print(result.json())

else:
    raise Exception('no access token in result')