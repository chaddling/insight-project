import requests
import json

# master list of apps on Steam
# -includes non-games ==> can filter out with keywords in genre tab in the app json page

apps_list_url = 'http://api.steampowered.com/ISteamApps/GetAppList/v2'
req_apps_list = requests.get(apps_list_url).json()

with open('../data/apps_list.json', 'w') as f:
    json.dump(req_apps_list, f)
