"""Takes inputs and creates forecast using a random forest model"""
import sqlalchemy as db
import psycopg2
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
# from sklearn.metrics import accuracy_score
# from sklearn import *
import numpy as np



class RandomForestRunner:
    """Takes inputs and creates forecasted probabilities using random forest"""
    def rforest(self, races, upcoming):
        """The random forest model builder"""
        try:
            engine = db.create_engine(
                'postgresql://postgres:postgres@localhost:5432/trav')
            connection = engine.connect()
            predictions = []

            for i in range(1, 8):

                class_var = races['class'][i]
                dst = races['distance'][i]
                start_mode = "'" + races['start'][i] + "'"

                max_track = upcoming[upcoming['race'] == i].shape[0]
                if max_track <= 12:
                    min_tr, max_tr = 1, 12
                else:
                    min_tr, max_tr = 13, 15
                query = f"with lopps as (select loppid from trav.maxtrack where max BETWEEN {min_tr} and {max_tr}) select a.won, a.track, a.winp, a.placep, a.betp, a.points, a.money, a.wincur from trav.flat_temp a where a.division LIKE {class_var}  and a.distance = {dst} and a.startmode = {start_mode}  and a.v75 IN ('1', '2', '3', '4', '5', '6', '7') and a.loppid IN (select loppid from lopps)"
                table = pd.read_sql(query, connection)

                if table.empty or len(table.index) < 50:
                    query = f"with lopps as (select loppid from trav.maxtrack where max BETWEEN {min_tr} and {max_tr}) select a.won, a.track, a.winp, a.placep, a.betp, a.points, a.money, a.wincur from trav.flat_temp a where  a.distance = {dst} and a.startmode = {start_mode}  and a.v75 IN ('1', '2', '3', '4', '5', '6', '7') and a.loppid IN (select loppid from lopps)"
                    table = pd.read_sql(query, connection)

                if table.empty or len(table.index) < 50:
                    query = f"select a.won, a.track, a.winp, a.placep, a.betp, a.points, a.money, a.wincur from trav.flat_temp a where  a.distance = {dst} and a.startmode = {start_mode}  and a.v75 IN ('1', '2', '3', '4', '5', '6', '7')"
                    table = pd.read_sql(query, connection)

                table = table.dropna()

                # x_train, x_test, y_train, y_test
                x_train, x_test, y_train, y_test = train_test_split(
                    table[['track', 'winp', 'placep', 'betp', 'points', 'money', 'wincur']], table['won'], test_size=0.25,
                    random_state=42, stratify=table['won'])

                n_estimators = [100, 200, 300]
                max_depth = [5, 8, 15, 25, 30]
                min_samples_split = [2, 5, 10, 15]
                min_samples_leaf = [1, 2, 5, 10]

                hyper_f = dict(n_estimators=n_estimators, max_depth=max_depth,
                              min_samples_split=min_samples_split,
                              min_samples_leaf=min_samples_leaf)

                forest = RandomForestClassifier(
                    random_state=1, n_estimators=10, min_samples_split=1)

                grid_f = GridSearchCV(forest, hyper_f, cv=3, verbose=1,
                                     n_jobs=-1)

                best_f = grid_f.fit(x_train, y_train)

                final_model = best_f.best_estimator_

                myrace = upcoming.loc[
                    upcoming['race'] == i, ['track', 'winp', 'placep', 'betp', 'points', 'money', 'wincur']]

                y_hat = final_model.predict_proba(myrace)

                y_hat = pd.DataFrame(y_hat)

                predictions = np.concatenate((predictions, y_hat[1]))

            upcoming['pred_win'] = predictions
            # print(accuracy_score(y_test, y_hat))

            return upcoming

        except Exception as exc:
            print(exc)

