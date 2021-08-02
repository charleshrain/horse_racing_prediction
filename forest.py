import sqlalchemy as db
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.model_selection import GridSearchCV


class forest:

    @classmethod
    def rforest(cls, races, upcoming):

        engine = db.create_engine(
            'postgresql://postgres:postgres@localhost:5432/trav')
        connection = engine.connect()

        for i in range(1, 7):

            cl = races['class'][i]
            dst = races['distance'][i]
            strt = races['start'][i]

            q = "select * from v75flat where division = '" + cl + \
                "' and distans = '" + dst + "' and startsatt = '" + strt + "'"

            table = pd.read_sql(q, connection)

            x_train, x_test, y_train, y_test = train_test_split(
                table.loc[:, table.columns != ['won', 'datum'], table['won'], test_size=0.25, random_state=42, stratify=table['won'])
            
            n_estimators = [100, 300, 500, 800, 1200]
            max_depth = [5, 8, 15, 25, 30]
            min_samples_split = [2, 5, 10, 15, 100]
            min_samples_leaf = [1, 2, 5, 10] 

            hyperF = dict(n_estimators = n_estimators, max_depth = max_depth,  
                        min_samples_split = min_samples_split, 
                        min_samples_leaf = min_samples_leaf)
            
            forest = RandomForestClassifier(random_state = 1, n_estimators = 10, min_samples_split = 1)

            gridF = GridSearchCV(forest, hyperF, cv = 3, verbose = 1, 
                                n_jobs = -1)
            
            bestF = gridF.fit(x_train, y_train)
            
            

            # param_grid = [
            #     {'n_estimators': [10, 25], 'max_features': [5, 10],
            #      'max_depth': [10, 50, None], 'bootstrap': [True, False]}
            # ]

            # upsampling, it is agued this should only be used on the traning set (change?):
            # https://datascience.stackexchange.com/questions/15630/train-test-split-after-performing-smote
            # table_majority = table[table.won==0]
            # table_minority = table[table.won==1]

            # table_minority_upsampled = resample(table_minority,
            #                      replace=True,     # sample with replacement
            #                      n_samples=len(table_majority.index),    # to match majority class
            #                      random_state=123) # reproducible results

            # table_upsampled = pd.concat([table_majority, table_minority_upsampled])
            # print(table_minority_upsampled)

            # train_test_split(X, y, random_state=0, stratify=y, shuffle=True)

            # classifier = RandomForestClassifier(n_estimators = 100, random_state = 0)
            # classifier.fit(table_upsampled['won'].reshape(-1, 1),table_upsampled['winperccurrent'].reshape(-1, 1))

            # # Number of trees in random forest
            # n_estimators = [int(x) for x in np.linspace(
            #     start=200, stop=2000, num=10)]
            # # Number of features to consider at every split
            # max_features = ['auto', 'sqrt']
            # # Maximum number of levels in tree
            # max_depth = [int(x) for x in np.linspace(10, 110, num=11)]
            # max_depth.append(None)
            # # Minimum number of samples required to split a node
            # min_samples_split = [2, 5, 10]
            # # Minimum number of samples required at each leaf node
            # min_samples_leaf = [1, 2, 4]
            # # Method of selecting samples for training each tree
            # bootstrap = [True, False]

            # random_grid = {'n_estimators': n_estimators,
            #                'max_features': max_features,
            #                'max_depth': max_depth,
            #                'min_samples_split': min_samples_split,
            #                'min_samples_leaf': min_samples_leaf,
            #                'bootstrap': bootstrap}

            # print(random_grid)

            # # Use the random grid to search for best hyperparameters
            # # First create the base model to tune
            # rf = RandomForestClassifier()
            # # Random search of parameters, using 3 fold cross validation,
            # # search across 100 different combinations, and use all available cores
            # rf_random = RandomizedSearchCV(estimator = rf, param_distributions = random_grid, n_iter = 100, cv = 3, verbose=2, random_state=42, n_jobs = -1)
            # # Fit the random search model
            # rf_random.fit(train_features, train_labels)

            # rf_random.best_params_
