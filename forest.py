import sqlalchemy as db
import pandas as pd
from sqlalchemy.engine.base import Transaction
from sklearn.utils import resample


class forest:

    @classmethod
    def rforest(cls, races, upcoming):

        engine = db.create_engine(
            'postgresql://postgres:postgres@localhost:5432/trav')
        connection = engine.connect()

        for i in range(1, 7):

            clas = races['class'][i]
            dist = races['distance'][i]
            strt = races['start'][i]

            q = "select * from v75flat where division = '" + clas + \
                "' and distans = '" + dist + "' and startsatt = '" + strt + "'"
                
            table = pd.read_sql(q, connection)
            
            table_majority = table[table.won==0]
            table_minority = table[table.won==1]
            
            table_minority_upsampled = resample(table_minority, 
                                 replace=True,     # sample with replacement
                                 n_samples=len(table_majority.index),    # to match majority class
                                 random_state=123) # reproducible results
            
            table_upsampled = pd.concat([table_majority, table_minority_upsampled])
            print(table_minority_upsampled)