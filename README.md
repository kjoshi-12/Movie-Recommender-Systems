# Movie-Recommender-Systems
This project consists of two different methods to recommend movies to a given user. 

1. Collaborative-Filtering

For this algorithm, this was developed in python. The heart of this algorithm is to recommend movies to a user based on another user's ratings that are the most similar to the given user. The similarity is calculated using cosine similarity formula, in which each similarity metric is stored in a matrix of every movie. For a respective user, a predicted rating for each movie is calculated, and if it is higher than 3.0, then it is considered to be a recommendation. This algorithm takes the top ten movies with the highest predicted ratings, and gives those as recommendations. 

Dependencies used in this project are

-SciPy
-Sklearn.metrics
