import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt

from eli5.sklearn import PermutationImportance

# compute the feature importances using the default implementation in sklearn's random forest.
# the default implementation uses gini importance averaged over all trees

# feature ames (used for plotting)
plot_label_names = ["# prerelease updates", "# post-release updates", "mean update time", "game description",
         "# of movies", "# of images", "action", "adventure", "casual", "mmo", "racing", "rpg",
         "simulation", "sports", "strategy"]

feature_names = ['num_pre', 'num_post', 'mean_time', 'len_description', 'num_movies', 'num_images', 'is_action', 'is_adventure',
           'is_casual', 'is_mmo', 'is_racing', 'is_rpg', 'is_simulation',
           'is_sports', 'is_strategy']

def get_label_names(indices, plot_label_names):
        return [plot_label_names[i] for i in indices]

# load model
with open('pickle_rf_model.pkl', 'rb') as file:
    rf = pickle.load(file)

data = pd.read_csv('data/features_vec_all.csv') # this does not include the no review ones

X = data[feature_names]

X = X.values
Y = data['sentiment'].values

# fit the model using the whole dataset
# with that we'll calculate the feature importances

rf[1].fit(X, Y)

# calculated over all leaves
importances = rf[1].feature_importances_
std = np.std([tree.feature_importances_ for tree in rf[1].estimators_], axis=0)

indices = np.argsort(importances)[::-1]

# Print the feature ranking
print("Feature ranking (default):")
for f in range(X.shape[1]):
    print("%d. feature %d (%f)" % (f + 1, indices[f], importances[indices[f]]))

## calculate the permutation importance
perm = PermutationImportance(rf[1]).fit(X, Y)
perm_importances = perm.feature_importances_
perm_indices = np.argsort(perm_importances)[::-1]

print("Permutation importances:")
for f in range(X.shape[1]):
    print("%d. feature %d (%f)" % (f + 1, perm_indices[f], perm_importances[perm_indices[f]]))

# Plot the feature importances of the forest
plt.figure()
plt.xlabel("Feature importances", fontsize=16)
plt.barh(range(X.shape[1]), list(reversed(importances[indices])),
       color="r", yerr=std[indices], align="center")
plt.yticks(range(X.shape[1]), list(reversed(get_label_names(indices, plot_label_names))), fontsize=14)
plt.ylim([-1, X.shape[1]])
plt.savefig('features_ranked.png')
plt.show()

plt.figure()
plt.xlabel("Permutation importances", fontsize=16)
plt.barh(range(X.shape[1]),list(reversed(perm_importances[perm_indices])),
       color="r", align="center")
plt.yticks(range(X.shape[1]), list(reversed(get_label_names(perm_indices, plot_label_names))), fontsize=14)
plt.ylim([-1, X.shape[1]])
plt.savefig('permutation_importances.png', bbox_inches='tight')
plt.show()
