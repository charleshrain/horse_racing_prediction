import sqlalchemy as db
from sqlalchemy.engine.base import Transaction

engine = db.create_engine(
            'postgresql://postgres:postgres@localhost:5432/trav')
connection = engine.connect()

class forest:
     @classmethod
     def rforest(cls, races, upcoming):
        for i in range(1,len(races.index)):
            print(races['class'][1])
            print(races['distance'][1])
            print(races['start'][1])
        print(upcoming)        
        metadata = db.MetaData()
        trot = db.Table('v75flat', metadata, autoload=True, autoload_with=engine)
        query = db.select([trot]).where(db.and_(trot.columns.state == 'California', trot.columns.sex != 'M'))
        ResultProxy = connection.execute(query)
        ResultSet = ResultProxy.fetchall()
        df = pd.DataFrame(ResultSet)
        df.columns = ResultSet[0].keys()