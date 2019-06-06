import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import re

from datetime import datetime, timedelta
from utils import parse_ratings, get_feature_vec

# games scraped through the steam API, we only care
game_data = pd.read_csv('data/my-gamedata.csv')
game_data = game_data.loc[game_data['is_indie']==1] # indie games only
game_data.drop(columns=['is_indie'], inplace=True)

game_updates = pd.read_csv('data/gamenews_updates-indie.csv', usecols=['game_id','timestamp'])
game_updates = game_updates[game_updates['timestamp']!=-1]
game_updates.set_index('data/game_id', inplace=True)

scraped_ratings = pd.read_csv('gamenews-indie.csv')
scraped_ratings.dropna(how='any',axis=0,inplace=True)

# call parse_ratings() to group the positive and negative sentiments together
ratings_parsed = parse_ratings(scraped_ratings)
ratings_parsed.drop_duplicates(inplace=True)

# games that have ratings through enough reviews
reviewed = ratings_parsed.loc[ratings_parsed['num_reviews'] >=10]
reviewed.set_index('game_id', inplace=True)

# games that have no ratings - not enough reviews
no_reviews = reviewed[reviewed['num_reviews'] <10]

# combine the raw datasets
features = get_feature_vec(game_data, game_updates, ratings_parsed)

# join feaures with ratings, drop uneeded rows
features_all = pd.merge(features, reviewed, how='inner', on='game_id')
features_all.drop(columns=['metacritic','recommendations','header_image'], inplace=True)
features_all.drop_duplicates(inplace=True)
features_all.dropna(how='any',axis=0,inplace=True)

features_nr = pd.merge(features, no_reviews, how='inner', on='game_id')
features_nr.drop(columns=['metacritic','recommendations','header_image'],inplace=True)
features_nr.drop_duplicates(inplace=True)
features_nr.dropna(how='any',axis=0,inplace=True)

 # there was a problem parsing this row when read again because of its title
features_vec_all = features_vec_all[features_vec_all['game_id']!=386710]

# save the output
features_all.to_csv('data/features_vec_all.csv',index=False)
features_nr.to_csv('data/features_vec_nr.csv',index=False)
