
from sqlalchemy import create_engine
import pandas as pd


class dbimport:
    columns = [
        'horseid',
        'datum',
        'bana',
        'trackno',
        'distans',
        'tillagg',
        'placering',
        'won',
        'winperccurrent',
        'winsperc',
        'placep',
        'tid',
        'mintid',
        'verklspar',
        'framspar',
        'startsatt',
        'division',
        'banforh',
        'avd75',
        'tvlid',
        'ownerwinperc',
        'moneyrank',
        'streckrank',
        'betperc',
        'tillaggmetre',
        'trainerwinperc',
        'pointsperc',
        'jockeyrank'
    ]

    @classmethod
    def import_data(cls):
        print("Importing...\n")
        # trav = pd.DataFrame(res.fetchall())
        engine = create_engine(
            'postgresql://postgres:postgres@localhost:5432/trav')
        file_name = 'data/v75flat.csv'
        df = pd.read_csv(file_name)
        df.columns = cls.columns
        df.to_sql(con=engine, index_label='id',
                name='v75flat', if_exists='replace')
