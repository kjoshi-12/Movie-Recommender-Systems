import csv
from scipy import spatial


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
        ratedMovies = []
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
                    ratedMovies = []
                    currentUser = userId
                    numUsers += 1

                try:
                    movieName = movies[movieId] # check if movieId exists
                    ratedMovies.append([movieId, movieRating])
                except KeyError:
                    numIgnored += 1 # certain movie ids are in ratings_small.csv, but not in movies_metadata.csv, so just ignore these ids

    userRatings[currentUser] = ratedMovies
    numUsers += 1

    return userRatings, numUsers

#Cosine Similarity computation: helps in choosing the movies that are most similar to another user's movie taste
def cosine_similarity(ratings_x, ratings_y):
    ratings_x_values = []
    ratings_y_values = []
    ratings_both = zip(ratings_x,ratings_y)
    for rating in ratings_both:
        curRating_x = rating[0][1]
        curRating_y = rating[1][1]
        ratings_x_values.append(curRating_x)
        ratings_y_values.append(curRating_y)
    result = 1 - spatial.distance.cosine(ratings_x_values, ratings_y_values)
    return result






movies, numMovies = readMovies()
userRatings, numUsers = readUserRatings(movies)
#Hard Coded Test Cases, specify a userId in the brackets of userRatings
ratings_x = userRatings[1]
ratings_y = userRatings[2]

similarity = cosine_similarity(ratings_x, ratings_y)
print(similarity)


