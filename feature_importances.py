import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt

# compute the feature importances using the default implementation in sklearn's random forest.
# the default implementation uses gini importance averaged over all trees

# feature ames (used for plotting)
names = ["# prerelease updates", "# post-release updates", "mean update time", "game description",
         "# of movies", "# of images", "action", "adventure", "casual", "mmo", "racing", "rpg",
         "simulation", "sports", "strategy"]

feature_names = ['num_pre', 'num_post', 'mean_time', 'len_description', 'num_movies', 'num_images', 'is_action', 'is_adventure',
           'is_casual', 'is_mmo', 'is_racing', 'is_rpg', 'is_simulation',
           'is_sports', 'is_strategy']

def get_feature_names(indices, feature_names):
        return [feature_names[i] for i in indices]

# load model
with open('pickle_rf_model.pkl', 'rb') as file:
    rf = pickle.load(file)

print(rf[1])

# load scaler
with open('pickle_scaler.pkl', 'rb') as file:
    scaler = pickle.load(file)

data = pd.read_csv('data/features_vec_all.csv') # this does not include the no review ones

X = data[feature_names]

# log transform on the data and rescale
X['num_pre'] = np.log(1 + 100*X['num_pre'])
X['num_post'] = np.log(1 + 200*X['num_post'])
X['mean_time'] = np.log(1 + 200*X['mean_time'])
X['len_description'] = np.log(1+X['len_description'])

X = X.values
Y = data['sentiment'].values

scaler.fit_transform(X[:,0:5])

# fit the model using the whole dataset
# with that we'll calculate the feature importances
rf[1].fit(X, Y)

# calculated over all leaves
importances = rf[1].feature_importances_
std = np.std([tree.feature_importances_ for tree in rf[1].estimators_], axis=0)

indices = np.argsort(importances)[::-1]

# Print the feature ranking
print("Feature ranking:")
for f in range(X.shape[1]):
    print("%d. feature %d (%f)" % (f + 1, indices[f], importances[indices[f]]))

# Plot the feature importances of the forest
plt.figure()
plt.ylabel("Feature importances", fontsize=16)
plt.bar(range(X.shape[1]), importances[indices],
       color="r", yerr=std[indices], align="center")
plt.xticks(range(X.shape[1]), get_feature_names(indices, names),rotation='vertical', fontsize=14)
plt.xlim([-1, X.shape[1]])
plt.savefig('features_ranked.png')
plt.show()
