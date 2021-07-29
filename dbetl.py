
from sqlalchemy import create_engine
import pandas as pd

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
    
engine = create_engine('postgresql://postgres:postgres@localhost:5432/trav')

file_name = 'data/v75flat.csv'
df = pd.read_csv(file_name)
df.columns=columns
df.to_sql(con=engine, index_label='id', name='v75flat', if_exists='replace')