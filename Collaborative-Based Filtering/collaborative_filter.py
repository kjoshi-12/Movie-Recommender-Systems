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


def generateMatrix(userRatings, numUsers):
    matrix = []
    for i in range(1, numUsers + 1):
        similarity = []
        for j in range(i + 1, numUsers + 1):
            ratings1 = userRatings[i]
            ratings2 = userRatings[j]
            user1Ratings, user2Ratings = determineVectors(ratings1, ratings2)

            sim = cosine_similarity(user1Ratings, user2Ratings)
            similarity.append(sim)
        matrix.append(similarity)
    return matrix

movies, numMovies = readMovies()
userRatings, numUsers = readUserRatings(movies)
#Hard Coded Test Cases, specify a userId in the brackets of userRatings
ratings_x = userRatings[1]
ratings_y = userRatings[2]

similarity = cosine_similarity(ratings_x, ratings_y)
print(similarity)

matrix = generateMatrix(userRatings, numUsers)

print(matrix[0])



