import pandas as pd

class PopularMovies:
  
  def noOfVotes(movies, rating):
    return pd.merge(movies, rating.groupby('movieId')["rating"].count().to_frame().rename(columns={'rating':'rating_Count'}), on = "movieId")
  
  def meanRatings(movies, rating):
    return pd.merge(movies, rating.groupby('movieId')["rating"].mean().to_frame().rename(columns={'rating':'rating_Average'}), on = "movieId")

  def meanVotes(movies): 
    return movies["rating_Average"].mean()
  
  def minVotes(movies):
    return movies["rating_Count"].quantile(0.98)

  def popularMoviesDataFrame(movies, m):
    return movies.copy().loc[movies['rating_Count'] >= m]

  def sortMoviesOnRanking(popularMovies, ranking):
    return popularMovies.sort_values(ranking, ascending=False)

  def getPopular(movies, co):
    C = movies["rating_Average"].mean()
    m = movies["rating_Count"].quantile(co)
    popMovies = movies.copy().loc[movies['rating_Count'] >= m]

    def weighted_rating(df, m=m, C=C):
      v = df["rating_Count"]
      R = df["rating_Average"]
      return (v / (v + m) * R) + (m / (v + m) * C) 

    popMovies['ranking'] = popMovies.apply(weighted_rating, axis=1)
    return popMovies.sort_values("ranking", ascending=False)