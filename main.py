import discord
from random import choice

with open ("secrets.txt", "r") as f:
    TOKEN = f.readline().strip()
    TOKEN = TOKEN.split("=")[1]

client = discord.Client()

def addMovie(message):
    movies = {}
    with open("movies.txt", "r", encoding="utf-8") as f:
        fileLines = f.readlines()
        for line in fileLines:
            line = line.strip()
            line = line.split(";")
            movies[line[0]] = line[1]
    
    movieName = message.content.split(" ",1)[1]

    if movieName in movies.keys():
        string = f"This movie was already added by {movies[movieName]}."
        return string 

    else:
        with open("movies.txt", "w", encoding="utf-8") as f:
            for key, value in movies.items():
                f.write(f"{key};{value}\n")
            f.write(f"{movieName};{message.author.name}\n")
        
        return "Movie added"

def removeMovie(message):
    movies = {}
    with open("movies.txt", "r", encoding="utf-8") as f:
        fileLines = f.readlines()
        for line in fileLines:
            line = line.strip()
            line = line.split(";")
            movies[line[0]] = line[1]
    
    movieName = message.content.split(" ",1)[1]

    if movieName in movies.keys():
        with open("movies.txt", "w", encoding="utf-8") as f:
            for key, value in movies.items():
                if key != movieName:
                    f.write(f"{key};{value}\n")
        return "Movie removed"
    else:
        return "Movie not found"

def listMovies(file):
    movies = {}
    with open(f"{file}.txt", "r", encoding="utf-8") as f:
        fileLines = f.readlines()
        for line in fileLines:
            line = line.strip()
            line = line.split(";")
            movies[line[0]] = line[1]
        
    string = ""

    for key, value in movies.items():
        string += f"{key}, added by {value}\n"

    string += "\n"
    string += f"Total movies: {len(movies)}"
    return string

def setWatchedMovie(message):
    movies = {}
    with open("movies.txt", "r", encoding="utf-8") as f:
        fileLines = f.readlines()
        for line in fileLines:
            line = line.strip()
            line = line.split(";")
            movies[line[0]] = line[1]
    
    movieName = message.content.split(" ",1)[1]

    try:
        # append the movie to the watched file
        with open("watchedMovies.txt", "a", encoding="utf-8") as f:
            f.write(f"{movieName};{movies[movieName]}\n")

        # delete the movie from the movies.txt file
        with open("movies.txt", "w", encoding="utf-8") as f:
            for key, value in movies.items():
                if key != movieName:
                    f.write(f"{key};{value}\n")

        return f"Movie \"{movieName}\" marked as watched"

    except:
        return "Movie not found"


@client.event
async def on_ready():
    print("Bot Loaded")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith("!addMovie"):
        await message.channel.send(addMovie(message))
        return
    
    if message.content.startswith("!removeMovie"):
        await message.channel.send(removeMovie(message))
        return
    
    if message.content.startswith("!listWatched"):
        await message.channel.send(listMovies("watchedMovies"))
        return
    
    if message.content.startswith("!listMovies"):
        await message.channel.send(listMovies("movies"))
        return
    
    if message.content.startswith("!watched"):
        await message.channel.send(setWatchedMovie(message))
        return

    if message.content.startswith("!random"):
       await message.channel.send(choice(listMovies("movies").split("\n")) ) 

    if message.content.startswith("!help"):
        await message.channel.send("""
        !addMovie <movie> - Add a movie to the list
!removeMovie <movie> - Remove a movie from the list
!listWatched - List all watched movies
!listMovies - List all movies
!watched <movie> - Mark a movie as watched
        """)

client.run(TOKEN)