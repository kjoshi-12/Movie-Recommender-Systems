import csv
import json

def writeMovies():
    with open("movies.csv", encoding="UTF-8") as csvFile:
        knowledgeBase = open("knowledge_base.pl", "w", encoding = "UTF-8")
        reader = csv.reader(csvFile)
        lines = 0
        for row in reader:
            if lines == 0:
                lines += 1
            else:
                genre = row[1].split("|")
                genre = [genre[i].strip() for i in range(len(genre))]    
                actors = row[2].split("|")
                size = len(actors) if len(actors) < 5 else 5
                actors = [actors[i].strip() for i in range(size)]
                companies = row[5].split("|")
                size = len(companies) if len(companies) < 3 else 3
                companies = [companies[i].strip() for i in range(size)]

                fact = "film({}, {}, {}, {}, {}, {}).\n".format(f'"{row[0]}"', ",".join(f'"{w}"' for w in genre), ",".join(f'"{w}"' for w in actors), f'"{row[3]}"', row[4], ",".join(f'"{w}"' for w in companies))
                knowledgeBase.write(fact)

movies = writeMovies()
