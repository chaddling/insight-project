# Insight project: indie.go
This is the project I worked on as an Insight Data Science Fellow, from ideation, data analysis, modeling to deploying a webapp which can be seen at [indie.go](http://3.13.31.175). The slides of the demo presentation can be found [here](https://tinyurl.com/y3xsxgz8).

# What it does
"Independent genre games", or indie games, are produced by small companies/developers and over the recent years there has been an exponential rise in the number of indie-genre games in the market. While the top earners in the genre remain successful, the median/mean sales and revenues have both gone down - that means a lot of the small developers simply don't get noticed on online vendor platforms.

Rather than tackling this from a recommendation system point of view, I developed indie.go as a tool to help developers assess how well they use their content page to attract users, releative to other indie games that have received positive reviews.

Showing to users that you as a game developer takes care of your content page presentation and that you interact with the players/address their concerns appeals to other users. Specifically, Steam has "Curator" accounts that have between 10-100k followers. Targeting these accounts for reviews - making them more likely to try your game - will have snowballing impact on your game's popularity.

# The data
The data I used were gather through Steam, one of the biggest online game vendors. I webscraped/queried through the Steam storefront/API. The code I used for gathering data are in [this folder](https://github.com/chaddling/insight-project/tree/master/scrape). It includes a scraper built using ``scrapy`` and simple API queries done in Python.

I processed the game content page data into a mix of ordinal/categorial features, these include:
- Number of gameplay videos shown
- Number of gameplay images shown
- Length of game description
- Number and frequencies of game updates
- Game genre keywords (these are one-hot encoded into 9 categories).

On top of that, once each game has received sufficient number of reviews, it receives a sentiment rating (Positive/Mixed/Negative) on Steam, which would give the game higher relevance in the recommendation system. The sentiment rating is related to the "% of positive reviews" that the game has received.

I scraped the game pages for both pages that are <b>labeled</b> as well as <b>unlabeled</b> games, which correspond to games that have received a sentiment rating/score and games have not.

# Modeling
Essentially, I trained/validated a classification model using the labeled game pages and their features, and used the model to label the unlabeled pages. This gives:

<b>i)</b> the % probability that the unlabeled page classifies as positive, which can be interpreted as a "similarity" score.

<b>ii)</b> the feature importance of the ordinal + categorical features - which are the features that I would recommend to the user of my product to pay attention to, in the order of importance determined by the model.

For this purpose, I used a multiclass Random Forest(RF) classifier implemented in ``scikit-learn``. The RF model has the added advantage of a ready-to-use implementation that computes feature importances.

In the [examples](https://github.com/chaddling/insight-project/tree/master/examples) folder, I included some basic analysis of the RF classifier against other simpler models (decision tree / logistic regression), as well as a regression model that I attempted: fitting the features to the "% positive score" instead.

The main script [train_rf_classifier.py](https://github.com/chaddling/insight-project/blob/master/train_rf_classifier.py) performs hyperparameter tuning and cross-validation, and evaluates the model on a held-out test dataset using ROC-AUC score. 

# Improvements
Given more time, it would be interesting to explore if the text content of the game description, or the content/aesthetics of the images/videos of the gameplay that is shown to the users. These are more powerful correlators to "attractiveness" of content presentation instead of the coarse-grained features I have used for the project.
