
from sqlalchemy import create_engine
import pandas as pd


class DatabaseImporter:
    columns = [
        'distance',
        'startmode',
        'division',
        'won',
        'track',
        'winp',
        'placep',
        'betp',
        'points',
        'money',
        'wincur'
    ]

    @classmethod
    def import_db_data(cls):
        print("Importing...\n")
        engine = create_engine(
            'postgresql://postgres:postgres@localhost:5432/trav')
        file_name = 'data/flat.csv'
        df = pd.read_csv(file_name)
        df.columns = cls.columns
        df.to_sql(con=engine, index_label='id',
                name='flat', if_exists='replace')
