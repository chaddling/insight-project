# combines the postive and negative sentiment scores together
# parse the strings columns in the csv table to get the % postiive score and number of reviewers for the game
def parse_ratings(scraped_ratings_df):

    j = 0
    df = pd.DataFrame(columns = ['game_id', 'score', 'num_reviews', 'sentiment'])

    sentiments = {"Overwhelmingly Positive":1, "Very Positive":1, "Positive":1, "Mostly Positive": 1,
                  "Mixed":0,
                  "Overwhelmingly Negative":-1, "Very Negative":-1, "Negative":-1, "Mostly Negative":-1
                 }

    for i, game in scraped_ratings_df.iterrows():
        g = game['p_reviews'].split()

        # get % positive response
        if g[3] != 'reviews':
            if len(g[3]) > 3:
                if g[3].find(',') > 0:
                    num_reviews = int(re.sub(',','',g[3]))
            else:
                num_reviews = int(g[3])
        else:
            num_reviews = 0

        if g[0].find('%') > 0:
            score = int(re.sub('%','',g[0]))*1.0/100
        else:
            score = 0

        if game['sentiment'] in sentiments.keys():
            sentiment = sentiments[game['sentiment']]
        else:
            sentiment = -2

        game_id = game['game_id']
        df.loc[j] = [game_id, score, num_reviews, sentiment]
        j += 1

    return df

# returns the feature_vector
def get_feature_vec(game_data_df, game_updates_df, ratings_parsed_df):

    j = 0
    features = pd.DataFrame(columns=['game_id', 'num_pre', 'num_post', 'mean_time', 'len_updates','num_movies', 'num_images'])

    for i, game in game_data_df.iterrows():
        game_id = game['game_id']
        release_date = game['release_date']
        num_movies = game['num_movies']
        num_images = game['num_screenshots']
        len_description = len(game['description'])

        if game_id in game_updates_df.index and game_id in ratings_parsed_df.index:
            update_times = game_updates_df.loc[game_id].timestamp

        # check if there are more than one updates
            if isinstance(update_times, np.ndarray):
                update_times = update_times.values
            elif isinstance(update_times, np.int64):
                update_times = np.array([update_times])

            update_times = np.append(update_times, release_date)
            update_times = np.sort(update_times)
            update_times = np.unique(update_times)

            if len(update_times) > 1:

            # counter separately updates pre and post game release
                cond_pre = update_times < release_date
                cond_post = update_times >= release_date

                num_updates_pre = len(np.where(cond_pre)[0])
                num_updates_post = len(np.where(cond_post)[0])

                mean_update_time = 0
                for i in range(0, len(update_times)-1): # some deltas are 0 (its release date patch)
                    delta_t = timedelta(seconds=int(update_times[i+1] - update_times[i])).days
                    mean_update_time += delta_t / (num_updates_pre + num_updates_post)

                features.loc[j] = [game_id, num_updates_pre, num_updates_post, mean_update_time, len_updates, num_movies, num_images]
                j+=1

    return features
