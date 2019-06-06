# Mine data via Steam API into SQL table
# - Game data: description field for each game_id

import requests
import json
import time
import re
import MySQLdb

# check if an app is a non-game software
def is_software(app_info, ids):
    if 'type' in app_info.keys():
        for t in app_info['type']:
            if t in software_ids:
                return True
    return False

# filter out non-game softwares and hardwares
software_ids = ['51', '52', '53', '54', '55', '56', '57', '58', '59']

# these are the steam defined game genres
genres = ['Action', 'Adventure', 'Casual', 'Indie', 'Massively Multiplayer',
            'Racing', 'RPG', 'Simulation', 'Sports', 'Strategy']

# master list of apps on steam
with open('../data/apps_list.json', "r") as f:
    apps_list = json.load(f)['applist']['apps']

# argument: id of game
url = 'https://store.steampowered.com/api/appdetails?appids={}'

# setup MySQL table
mysql_connection = MySQLdb.connect(host='localhost',
                                    database='steamstats',
                                    user='chaddling',
                                    password=' ',
                                    use_unicode=True,
                                    charset="utf8")

mysql_cursor = mysql_connection.cursor()

for app in apps_list:
    app_id = app['appid']
    app_url = url.format(app_id)

    app_request = requests.get(app_url)
    app_json = app_request.json()

    while app_json == None:
        # request the json again after a timeout if it was not successful
        time.sleep(30.0)
        print('timed out, waiting for 30s\n')
        app_request = requests.get(app_url)
        app_json = app_request.json()

    app_json = app_json[str(app_id)]

    # json is read successfuly
    if app_json['success']:
        app_info = app_json['data']
        is_game = (app_info['type'] == 'game')

        if is_game and not is_software(app_info, software_ids):
            genre_vec = dict(zip(genres, [0]*10))

            # remove non-ascii chars
            game_title = re.sub(r'([^\x00-\x7f]|")', r'', app_info['name'])

            raw_description = app_info['about_the_game']
            # remove html and non-ascii characters from game description
            description = re.sub(r'([^\x00-\x7f]|"|<[^<]+?>)', r' ', raw_description)

            header_image = app_info['header_image']

            score = 0
            if 'metacritic' in app_info.keys():
                score = app_info['metacritic']['score']

            rec = 0
            if 'recommendations' in app_info.keys():
                rec = app_info['recommendations']['total']

            if 'genres' in app_info.keys():
                for g in app_info['genres']:
                    genre_vec[g['description']] = 1

            genre_list = list(genre_vec.values())

            insert = "INSERT INTO gamedata(`game_id`, `game_title`, `game_description`, `metacritic`, `release_date`, `num_movies`, `num_images`,`recommendations`, `header_image`, `is_action`, `is_adventure`, `is_casual`, `is_indie`, `is_mmo`, `is_racing`, `is_rpg`, `is_simulation`, `is_sports`, `is_strategy`) \
                        VALUES(\"{}\", \"{}\",\"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\")".format(app_id, game_title, description, score, rec, header_image, *genre_list)
            print('inserting', app_id)
            mysql_cursor.execute(insert)
            mysql_connection.commit()

mysql_connection.close()
