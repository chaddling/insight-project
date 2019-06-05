import pandas as pd
import numpy as np
import pickle

from collections import Counter
from sklearn.preprocessing import label_binarize, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV, train_test_split, StratifiedKFold
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline

n_classes = 3

data = pd.read_csv('data/features_vec_all.csv')

feature_names = ['num_pre', 'num_post', 'mean_time', 'len_description',
       'num_movies', 'num_images', 'is_action', 'is_adventure',
       'is_casual', 'is_mmo', 'is_racing', 'is_rpg', 'is_simulation',
       'is_sports', 'is_strategy']

X = data[feature_names].values
Y = data['sentiment'].values

scaler = StandardScaler(copy=False)
scaler.fit_transform(X[:,0:5])

#Y = label_binarize(Y, classes=[-1,0,1])


# Y_hold Counter({1.0: 1710, 0.0: 613, -1.0: 88}  for n_reviews > 50
X_train, X_hold, Y_train, Y_hold = train_test_split(X, Y, test_size=0.4)

sm = SMOTE()
rf = RandomForestClassifier()

# define pipeline which performs oversampling with SMOTE
# and then the random foest classifier
pipeline = Pipeline([('sm', sm), ('rf', rf)])

kf = StratifiedKFold(n_splits=5)

params = {'rf__n_estimators': list(range(5,20)),
          'rf__max_depth': list(range(5,20))}

grid = GridSearchCV(estimator=pipeline,
                    param_grid=params,
                    scoring='f1_macro',
                    cv=kf,
                    n_jobs=2)

# after hyperparameter optimization, train on the held out data
grid.fit(X_hold, Y_hold)

pkl_filename = "pickle_rf_model.pkl"
with open(pkl_filename, 'wb') as file:
    pickle.dump(rf, file)

scl_filename = "pickle_scaler.pkl"
with open(scl_filename, 'wb') as file:
    pickle.dump(scaler, file)
