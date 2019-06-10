import pandas as pd
import numpy as np
import pickle

from sklearn.preprocessing import label_binarize, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV, train_test_split, StratifiedKFold
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline

from plot_roc import plot_roc_curve

# traing the random forest classifier

n_classes = 3

data = pd.read_csv('data/features_vec_all.csv')

feature_names = ['num_pre', 'num_post', 'mean_time', 'len_description',
       'num_movies', 'num_images', 'is_action', 'is_adventure',
       'is_casual', 'is_mmo', 'is_racing', 'is_rpg', 'is_simulation',
       'is_sports', 'is_strategy']

X = data[feature_names]

# log transform on the data and rescale
X['num_pre'] = np.log(1 + 100*X['num_pre'])
X['num_post'] = np.log(1 + 200*X['num_post'])
X['mean_time'] = np.log(1 + 200*X['mean_time'])
X['len_description'] = np.log(1+X['len_description'])

X = X.values
Y = data['sentiment'].values

# rescale only the continuous variables by (x- mu) / std
scaler = StandardScaler(copy=False)
scaler.fit_transform(X[:,0:5])

#Y = label_binarize(Y, classes=[-1,0,1])

# split the data:
# 1. training data is then further over sampled in the pipeline then split up
# during hyperparametertuning/CV
# 2. test data will preserve the class proportion in the original data
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, stratify=Y, test_size=0.2)

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

grid.fit(X_train, Y_train)


print(grid.best_estimator_)
print('best score = ', grid.best_score_)
cv_results = grid.cv_results_

print('mean_score +/- std =', cv_results['mean_test_score'].mean(), cv_results['std_test_score'].mean())


Y_score = grid.predict_proba(X_test)

# one-hot encode the classes
Y_test = label_binarize(Y_test, classes=[-1,0,1])

print(Y_score.shape, Y_test.shape)

# evaluate the model on AUC score on the test data
plot_roc_curve(3, Y_test, Y_score)


pkl_filename = "pickle_rf_model.pkl"
with open(pkl_filename, 'wb') as file:
    pickle.dump(grid.best_estimator_, file)

scl_filename = "pickle_scaler.pkl"
with open(scl_filename, 'wb') as file:
    pickle.dump(scaler, file)
