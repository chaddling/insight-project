import requests
import json
import time
import re
import pandas as pd

from datetime import datetime
from json.decoder import JSONDecodeError

#steam_API_key = '6313242389C9E6D644A896AB15BDAB6D'

# arguments: game_id
#store_url = 'https://store.steampowered.com/api/appdetails?appids={}'
news_url = 'http://api.steampowered.com/ISteamNews/GetNewsForApp/v0002/?appid={}'

# two DFs to aggregate information
# will need to process 'update_content' to find the TYPE of update it is (bug fix, patch, etc...)
# same number of rows for both
#game_summary = pd.DataFrame(columns = ['game_id', 'num_screenshots', 'num_movies', 'relase_date'])
game_news_df = pd.DataFrame(columns = ['game_id', 'timestamp', 'update_content'])

# master list of games (indie only)
my_game_data = pd.read_csv('../data/my-gamedata.csv', usecols = ['game_id', 'is_indie'])
my_game_data = my_game_data[my_game_data['is_indie'] == 1]
my_game_data = my_game_data.reset_index(drop=True)

# convert month string to int
months = {'Jan': '1', 'Feb': '2', 'Mar': '3', 'Apr': '4', 'May': '5',
            'Jun': '6', 'Jul': '7', 'Aug': '8', 'Sep': '9', 'Oct': '10',
            'Nov': '11', 'Dec': '12'}

#game_summary_output = '../data/gamepage_summary_indie.csv'
game_news_output = '../data/gamenews_updates_indie.csv'

last_index = 0
last_id = 556870


with open(game_news_output, 'w') as g:
    g.write('game_id,timestamp,update_label,update_content\n')
g.close()

# main
for i, game in my_game_data.iterrows():
    game_id = game['game_id']

    # get news
    print('fetching game news for ', game_id)

    game_news_url = news_url.format(game_id)
    game_news_request = requests.get(game_news_url)
    game_news_json = game_news_request.json()

    if 'appnews' in game_news_json.keys():
        game_news_page = game_news_json['appnews']

        num_of_news = game_news_page['count']

        if num_of_news > 0:
            all_news_url = game_news_url + '&count={}'.format(num_of_news)
            game_news_request = requests.get(all_news_url)
            game_news_json = game_news_request.json()
            game_news_page = game_news_json['appnews']

            for news in game_news_page['newsitems']: # scrape every news item
                timestamp = news['date'] # this is in posix
                content = news['contents'] # description of the news, lets take the whole thing...
                content = re.sub(r'([^\x00-\x7f]|")', r'', content)
                content = re.sub(r'\n|\t|\r|,', r' ', content)

                # reviews in major blogs (kotaku , rps, eurogamer, pc games)
                # are labeled
                label = news['feedlabel']
                label = re.sub(r',', r' ', label)

                with open(game_news_output,'a+') as g:
                    g.write('{},{},{},\"{}\"\n'.format(game_id, timestamp, label, content))
                g.close()

        else: # has news page but no news items
                with open(game_news_output,'a+') as g:
                    g.write('{},{},{},\"{}\"\n'.format(game_id, -1, ' ', ' '))
                g.close()
    else: # has no news page (== {})
        with open(game_news_output,'a+') as g:
            g.write('{},{},{},\"{}\"\n'.format(game_id, -1, ' ', ' '))
        g.close()
