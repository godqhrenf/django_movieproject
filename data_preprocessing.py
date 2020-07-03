import pandas as pd
# from sqlalchemy import create_engine
import sqlite3

def csvToMySQL():
    df = pd.read_csv('./data/tmdb_ratings.csv')
    tableName = 'moviereco_movierating'
    engine = sqlite3.connect("C:/Users/kmy/django/db.sqlite3")
    df.to_sql(name=tableName, con=engine, if_exists='append', index=False)


if __name__ == '__main__':



'''
new = {'userId': [700], 'movieId': [489], 'rating': [4.0]}
df = pd.DataFrame(new)
tableName = 'movie_movie'
engine = sqlite3.connect("C:/Users/kmy/django/db.sqlite3")
df.to_sql(name=tableName, con=engine, if_exists='append', index=False)
'''

