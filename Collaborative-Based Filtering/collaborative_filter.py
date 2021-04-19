import csv

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


movies, numMovies = readMovies()
userRatings, numUsers = readUserRatings(movies)

