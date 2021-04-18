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

def readUserRatings(movies, numMovies):
    userRatings = {}
    sortedMovies = list(movies.values())
    sortedMovies.sort()

    with open("ratings_small.csv", encoding="UTF-8") as csvFile:
        reader = csv.reader(csvFile)
        lines = 0
        ratedMovies = [0] * numMovies
        currentUser = 1
        numIgnored = 0
        for row in reader:
            if lines == 0:
                lines += 1
                continue
            else:
                userId, movieId, movieRating = int(row[0]), int(row[1]), float(row[2])
                if userId != currentUser:
                    userRatings[currentUser] = ratedMovies
                    ratedMovies = [0] * numMovies
                    currentUser = userId

                try:
                    movieName = movies[movieId]
                    index = sortedMovies.index(movieName)
                    ratedMovies[index] = movieRating
                except KeyError:
                    numIgnored += 1 # certain movie ids are in ratings_small.csv, but not in movies_metadata.csv, so just ignore these ids
        
    return userRatings


movies, numMovies = readMovies()
userRatings = readUserRatings(movies, numMovies)


