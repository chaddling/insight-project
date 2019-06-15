# Insight project: indie.go
This is the project I worked on as an Insight Data Science Fellow, from ideation, data analysis, modeling to deploying a webapp which can be seen at [indie.go](http://3.13.31.175). The slides of the demo presentation can be found [here](https://docs.google.com/presentation/d/e/2PACX-1vQ4grjTdVG8p0DdcCGoHgg7qJA5PeqIHgSYGvmCRxjaP7nLXPPd_ILKI-F0FPCxVdfZ9BUkdwbxuS3N/pub?start=false&loop=false&delayms=15000).

# What it does
"Independent genre games", or indie games, are produced by small companies/developers and over the recent years there has been an exponential rise in the number of indie-genre games in the market. While the top earners in the genre remain successful, the median/mean sales and revenues have seen a > 50% decrease - that means a lot of the small developers simply don't get noticed on online vendor platforms.

Rather than tackling this from a recommendation system point of view, I developed indie.go as a tool to help developers assess how well they use their content page to attract users, releative to other indie games that have received positive reviews.

Showing to users that you as a game developer takes care of your content page presentation and that you interact with the players/address their concerns appeals to other users. Specifically, Steam has "Curator" accounts that have between 10-100k followers. Targeting these accounts for reviews - making them more likely to try your game - will have snowballing impact on your game's popularity.

# The data
The data I used were gather through Steam, one of the biggest online game vendors. 

I webscraped/queried through the Steam storefront/API for content items of indie game pages. The code I used for gathering data are in [this folder](https://github.com/chaddling/insight-project/tree/master/scrape). It includes a scraper built using ``scrapy`` and simple API queries done in Python.

I processed the game content page data into a mix of continuous, ordinal/one-hot encoded categorical features, these include:

- Number of gameplay videos shown
- Number of gameplay images shown
- Length of game description
- Number and frequencies of game updates
- Game genre keywords (9 categories).

On top of that, once each game has received sufficient number of reviews, it receives a sentiment rating (<b>Positive/Mixed/Negative</b>) on Steam, which would give the game higher relevance in the recommendation system. The sentiment rating is related to the "% of positive reviews" that the game has received.

I scraped the game pages for both pages that are <b>labeled</b> as well as <b>unlabeled</b> games, which correspond to games that have received a sentiment rating/score and games that have not.

# Modeling
I trained a classification model using the labeled game pages and their features, and used the model to label the unlabeled pages. This gives:

<b>i)</b> the % probability that the unlabeled page classifies as positive, which can be interpreted as a "similarity" score.

<b>ii)</b> the feature importance of the ordinal + categorical features - which are the features that I would recommend to the user of my product to pay attention to, in the order of importance determined by the model.

For this purpose, I used a multiclass Random Forest(RF) classifier implemented in ``scikit-learn``. The RF model has the added advantage of a ready-to-use implementation that computes feature importances.

In the [examples](https://github.com/chaddling/insight-project/tree/master/examples) folder, I included some basic analysis of the RF classifier against other simpler models (decision tree / logistic regression), as well as a regression model that I attempted: fitting the features to the "% positive score" instead.

The main script [train_rf_classifier.py](https://github.com/chaddling/insight-project/blob/master/train_rf_classifier.py) performs hyperparameter tuning and cross-validation, and evaluates the model on a held-out test dataset using ROC-AUC score. 

# Diagnostics
Given the low performance of the model and the nature of the data, I was suspicious of the default feature importance output generate by the Random Forest model:

![](https://raw.githubusercontent.com/chaddling/insight-project/master/png/features_ranked.png)

In tree-based models, because continuous/high-cardinality features can be split in more ways than one-hot encoded ones, this generates a bias in feature importances calculated based on Gini impurity (the default method) when the features are of mixed types.

I performed feature importance analysis using a permutation-based method, which calculates for each feature, the mean change in model performance when the values of that feature are randomly permuted.

![](https://raw.githubusercontent.com/chaddling/insight-project/master/png/permutation_importances.png)

Overall, each feature receives very low importance score, which explains the model performance. 

Despite the weak importance scores, a genre feature (MMO = "massively online multiplayer") stood out: this type of game, due to the online nature of its play, tends to have high number of updates / high update frequency (as regular maintenance is neccessary). Further analysis (see boxplots in [png](https://github.com/chaddling/insight-project/tree/master/png) folder) shows that they contribute most strongly to the outliers in the distributions of other features and this increased the discriminative power of the model.

The code for calculating feature importances is found in [feature_importances.py](https://github.com/chaddling/insight-project/blob/master/feature_importances.py) and in the notebook [permutation_importance.ipynb](https://github.com/chaddling/insight-project/blob/master/examples/permutation_importance.ipynb) I did an implementation of permutation importance on my own.

# Improvements
<b> Other features </b>

Given more time, it would be interesting to explore if the text content of the game description, or the content/aesthetics of the images/videos of the gameplay that is shown to the users. These are more powerful correlators to "attractiveness" of content presentation instead of the coarse-grained features I have used for the classification approach.
