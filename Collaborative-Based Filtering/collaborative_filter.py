import csv
from scipy import spatial
from sklearn.metrics import mean_squared_error
import math


def readMovies():
    movies = {}
    numMovies = 0
    with open("movies.csv", encoding="UTF-8") as csvFile:
        reader = csv.reader(csvFile)
        lines = 0
        for row in reader:
            if lines == 0:
                lines += 1
            else:
                movies[int(row[0])] = row[1]
                numMovies += 1      
    
    return movies, numMovies

def readUserRatings(movies):
    userRatings = {}

    with open("ratings_small.csv", encoding="UTF-8") as csvFile:
        reader = csv.reader(csvFile)
        lines = 0
        ratedMovies = {}
        currentUser = 1
        numUsers = 0
        numIgnored = 0
        for row in reader:
            if lines == 0:
                lines += 1
                continue
            else:
                userId, movieId, movieRating = int(row[0]), int(row[1]), float(row[2])
                if userId != currentUser:
                    userRatings[currentUser] = ratedMovies
                    ratedMovies = {}
                    currentUser = userId
                    numUsers += 1

                try:
                    movieName = movies[movieId] # check if movieId exists
                    ratedMovies[movieId] = movieRating
                except KeyError:
                    numIgnored += 1 # certain movie ids are in ratings_small.csv, but not in movies_metadata.csv, so just ignore these ids

    userRatings[currentUser] = ratedMovies
    numUsers += 1

    return userRatings, numUsers

def determineVectors(ratings1, ratings2):
    user1Movies = list(ratings1.keys())
    user2Movies = list(ratings2.keys())
    movies = list(set(user1Movies) | set(user2Movies))

    user1Ratings = []
    for id in movies:
        try:
            rating = ratings1[id]
        except KeyError:
            rating = 0
        user1Ratings.append(rating)

    user2Ratings = []
    for id in movies:
        try:
            rating = ratings2[id]
        except KeyError:
            rating = 0
        user2Ratings.append(rating)
    return user1Ratings, user2Ratings

#Cosine Similarity computation: helps in choosing the movies that are most similar to another user's movie taste
def cosine_similarity(ratings_x, ratings_y):
    result = 1 - spatial.distance.cosine(ratings_x, ratings_y)
    return result

#Root Mean Squared Error: Evaluation metric testing how well the rating prediction was to the actual rating
def root_mean_squared_error(actual_ratings, predicted_ratings):
    rmse = math.sqrt(mean_squared_error(actual_ratings, predicted_ratings))
    return rmse


def generateMatrix(userRatings, numUsers):
    matrix = []
    for i in range(1, numUsers + 1):
        similarity = []
        for j in range(1, numUsers + 1):
            ratings1 = userRatings[i]
            ratings2 = userRatings[j]
            user1Ratings, user2Ratings = determineVectors(ratings1, ratings2)
            sim = cosine_similarity(user1Ratings, user2Ratings)
            similarity.append([sim, j])
        matrix.append(similarity)
    return matrix

def determineRating(similarityMatrix, userRatings, userId, movieId, numSimilarUsers):
    sortedSimilarities = sorted(similarityMatrix[userId - 1], reverse = True, key = lambda sim: sim[0])

    index = 0
    k = 0
    ratingSum = 0
    similaritySum = 0
    while k < numSimilarUsers and index < len(sortedSimilarities):
        simUserId = sortedSimilarities[index][1]
        if simUserId == userId:
            index += 1
            continue
        userMovies = userRatings[simUserId]
        if movieId in userMovies:
            ratingSum += (sortedSimilarities[index][0] * userMovies[movieId])
            similaritySum += sortedSimilarities[index][0]
            k += 1
        index += 1
    #similaritySum = 0
    try:
        determined_rating = ratingSum / similaritySum
    except ZeroDivisionError:
        determined_rating = 0
    return determined_rating

#Function to retrieve the movieId given the title
def get_movieId(title,dict):
    for id, movie_title in dict.items():
         if title == movie_title:
             return title

def main():
    movies, numMovies = readMovies()
    userRatings, numUsers = readUserRatings(movies)

    matrix = generateMatrix(userRatings, numUsers)


    read_user = int(input("Please enter User ID: "))
    current_user = read_user   #The active user on the service


    #Main process: Finds recommended movies
    predicted_recommended_movies = {}
    movieId_iterator = 1
    while movieId_iterator < numMovies:
        predicted_rating = determineRating(matrix, userRatings, current_user, movieId_iterator, 10)
        user_ratings = userRatings[1]
        if predicted_rating >= 3.0 and (movieId_iterator in user_ratings):
            # Add movie to recommended movies data stuct
            predicted_recommended_movies[movies[movieId_iterator]] = predicted_rating
        movieId_iterator += 1

    #Sorts the recomendations based on the predicted rating
    prm_sorted = {movie_title: rating for movie_title, rating in sorted(predicted_recommended_movies.items(), reverse=True, key=lambda item: item[1])}
    print(prm_sorted)

    #Obtains top 10 movies
    recommended_movies = prm_sorted.items()
    top_10 = list(recommended_movies)[:10]
    recommendations = []
    predicted_ratings = []
    for movie_rating in top_10:
        recommendations.append(movie_rating[0])
        predicted_ratings.append(movie_rating[1])

    #Prints recommended movies to the console
    print("\nHere are your recommended movies:")
    for recommendation in recommendations:
        print(recommendation)

    #Gets the actual ratings of the movies
    actual_ratings = []
    for title in recommendations:
        movie_id = get_movieId(title,movies)
        user_ratings = userRatings[1]
        try:
            actual_ratings.append(user_ratings[movie_id])
        except KeyError:
            actual_ratings.append(0)
    print(actual_ratings)
    # accuracy = root_mean_squared_error(actual_ratings,predicted_ratings)
    # print("Accuracy of predictions/recommendations: {}".format(accuracy))

if __name__ == "__main__":
    main()