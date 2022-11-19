import pandas as pd
from collections import Counter

# Data Retrieving
file_content = pd.read_csv('ratings.csv', sep='\t', usecols=['user_id', 'movie_id', 'rating'])


# Data Formatting for analyzing
content = pd.DataFrame(file_content).head(300)

users = content["user_id"]
movies = content["movie_id"]
ratings = content["rating"]

user = []
for k in users.values:
    user.append(k)
print("Total no. of users: {}".format(len(user)))

movie = []
for k in movies.values:
    movie.append(k)

print("Total no. of movies: {}".format(len(movie)))

rating = []
for k in ratings.values:
    rating.append(k)

print("Ratings in unique: {}".format(len(set(rating))))


# Movies and its corresponding rating

movie_rating = {}

unique_rate = set(rating)
for i in unique_rate:
    mov = []
    for k, v in zip(movie, rating):
        if i == v:
            mov.append(k)
    movie_rating.update({i: mov})

print("Rating with list of movies")
for k, v in movie_rating.items():
    print(k, "-->", v)


# Users with watched rating
user_rating = {}

unique_rate = set(rating)
for i in unique_rate:
    mov = []
    for k, v in zip(user, rating):
        if i == v:
            mov.append(k)
    user_rating.update({i: mov})

print("Rating with users")
for k, v in user_rating.items():
    print(k, "-->", v)

# Users with their already watched list
user_movie = {}

unique_user = set(user)
print("Printing unique user ids: {}".format(unique_user))
for i in unique_user:
    mov = []
    for k, v in zip(user, movie):
        if i == k:
            mov.append(v)
    user_movie.update({i: mov})

print("Users with their watched movies")
for k, v in user_movie.items():
    print(k, "-->", v)

# Counting the specific number of users in each rating
most_watched = {}
for k, v in user_rating.items():
    d = Counter(v)
    most_watched.update({k: d})
print(most_watched)


def exclude_already_watched(list, user_id):
    for k, v in user_movie.items():
        if k == user_id:
            already_watched = v
    watch = []
    for i in list:
        if i in already_watched:
            continue
        else:
            watch.append(i)
    return watch


# Only user specific data
def user_specific(user_id):
    high = 0
    rate = 0
    for k, v in most_watched.items():
        for i, j in v.items():
            if i == user_id:
                if j > high:
                    high = j
                    rate = k
    return high, rate


def movie_recommendation(user_id):
    high_no, high_rate = user_specific(user_id)
    val = high_rate
    print("Most interested rating: {}".format(high_rate))
    rate_list_movies = movie_rating.get(val)
    recommend_list = exclude_already_watched(rate_list_movies, user_id)
    return recommend_list


user_id = int(input("Enter user login: "))
for i in unique_user:
    if i == user_id:
        break
else:
    print(f"Mentioned user_id {user_id} is not in the given data range list")
    exit()

recommended_list = movie_recommendation(user_id)
print(f"Recommended List for User {user_id} is {recommended_list}")
