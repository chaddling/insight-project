import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import re

from datetime import datetime, timedelta

# games scraped through the steam API, we only care
game_data = pd.read_csv('my-gamedata.csv')
game_data = game_data[game_data['is_indie']==1] # indie games only
game_data.drop(columns=['is_indie'], inplace=True)

game_updates = pd.read_csv('gamenews_updates-indie.csv', usecols=['game_id','timestamp'])
game_updates = game_updates[game_updates['timestamp']!=-1]

scraped_ratings = pd.read_csv('gamenews-indie.csv')
scraped_ratings.dropna(how='any',axis=0,inplace=True)
