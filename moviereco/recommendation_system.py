from sklearn.decomposition import TruncatedSVD
from scipy.sparse.linalg import svds
import pandas as pd
import numpy as np

import sqlite3

def svdMatFactorization():
    engine = sqlite3.connect("C:/Users/kmy/django/db.sqlite3")
    df_rating = pd.read_sql('SELECT * FROM moviereco_movierating', engine, index_col='id')
    df_user_movie_rating = df_rating.pivot(index = 'userId', columns = 'movieId', values = 'rating').fillna(0)

    matrix = df_user_movie_rating.values
    user_rating_mean = np.mean(matrix, axis = 1)
    matrix_user_mean = matrix - user_rating_mean.reshape(-1, 1)

    U, sigma, Vt = svds(matrix_user_mean, k=12)
    sigma = np.diag(sigma)
    svd_user_predicted_rating = np.dot(np.dot(U, sigma), Vt) + user_rating_mean.reshape(-1, 1)
    df_svd_preds = pd.DataFrame(svd_user_predicted_rating, columns = df_user_movie_rating.columns)

    return df_rating, df_svd_preds

def recommendMovies(user_id, num_recommendations=5):
    ori_ratings_df, df_svd_preds = svdMatFactorization()

    # index로 설정해야하므로 user_id - 1 해줘야 함
    user_row_number = user_id - 1

    # user_id에 해당하는 prediction만 뽑아줌
    user_predictions = pd.DataFrame(df_svd_preds.iloc[user_row_number]).reset_index()

    # user_id에 해당하는 원래 평점 데이터만 뽑아줌
    user_data = ori_ratings_df[ori_ratings_df.userId == user_id]

    # prediction에서 사용자가 본 영화는 걸러줌
    recommendations = user_predictions[~user_predictions['movieId'].isin(user_data['movieId'])]

    # column이름을 바꾸고 평점이 높은 순으로 정렬해서 리턴
    recommendations = recommendations.rename(columns = {user_row_number: 'Predictions'}
                                            ).sort_values('Predictions', ascending = False).iloc[:num_recommendations, :]

    # dataframe을 json 형식으로 바꿔서 리턴
    return recommendations.to_json(orient='values')