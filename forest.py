import sqlalchemy as db
import pandas as pd
from sqlalchemy.engine.base import Transaction


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
            # print(table)
