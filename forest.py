import sqlalchemy as db
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
# from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import train_test_split
# from sklearn.metrics import mean_squared_error
from sklearn import *
import numpy as np
from sklearn.model_selection import GridSearchCV


class forest:
    
    @classmethod
    def rforest(cls, races, upcoming):

        engine = db.create_engine(
            'postgresql://postgres:postgres@localhost:5432/trav')
        connection = engine.connect()
        
        predictions = []

        for i in range(1, 8):

            cl = races['class'][i]
            dst = races['distance'][i]
            strt = races['start'][i]

            q = "select flat.won, flat.track, flat.winp, flat.placep, flat.betp, flat.points, flat.money from trav.flat where distance = '" + dst + "' and startmode = '" + strt + "'"

            table = pd.read_sql(q, connection)
            
            table = table.dropna()

            x_train, x_test, y_train, y_test = train_test_split(
                table[['track', 'winp', 'placep', 'betp', 'points', 'money']], table['won'], test_size=0.25, random_state=42, stratify=table['won'])
            

            n_estimators = [100]
            max_depth = [5, 8, 15, 25, 30]
            min_samples_split = [2, 5, 10, 15]
            min_samples_leaf = [1, 2, 5, 10]

            hyperF = dict(n_estimators=n_estimators, max_depth=max_depth,
                          min_samples_split=min_samples_split,
                          min_samples_leaf=min_samples_leaf)

            forest = RandomForestClassifier(
                random_state=1, n_estimators=10, min_samples_split=1)

            gridF = GridSearchCV(forest, hyperF, cv=3, verbose=1,
                                 n_jobs=-1)

            bestF = gridF.fit(x_train, y_train)
               
            final_model = bestF.best_estimator_
            
            myrace = upcoming.loc[upcoming['race'] == i,[ 'track', 'winp', 'placep', 'betp', 'points', 'money']]
        
            y_hat = final_model.predict(myrace)
            
            predictions = np.concatenate((predictions, y_hat))
            
            
        upcoming['pred'] = predictions
        
        return upcoming
            
           
            