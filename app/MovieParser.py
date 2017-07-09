import os
import json
import random

MovieFile = './static/Assets/movie.json'

def GetMovieInfo(movieID):
    movieDict = {}

    with open(MovieFile) as json_data:
        json_object = json.load(json_data)

        movieDict['STUDIO_NAME'] = json_object[movieID].get('STUDIO_NAME')
        movieDict['ROLE'] = json_object[movieID].get('ROLE')
        movieDict['TALENT_NAME'] = json_object[movieID].get('TALENT_NAME')
        movieDict['CONTENT_TITLE'] = json_object[movieID].get('CONTENT_TITLE')
        movieDict['POSTER_URL'] = json_object[movieID].get('POSTER_URL')
        movieDict['CONTENT_TYPE'] = json_object[movieID].get('CONTENT_TYPE')
        movieDict['GENRE'] = random.choice(json_object[movieID].get('GENRE').split(',')).replace('amp;', '')
        movieDict['RATING'] = json_object[movieID].get('RATING')
        movieDict['PARENT_CID'] = json_object[movieID].get('PARENT_CID')
        # if movieDict['PARENT_CID']:
        #     parent_title = json_object[json_object[movieID].get('PARENT_CID')].get('CONTENT_TITLE')
        #     if parent_title:
        #         movieDict['CONTENT_TITLE'] = parent_title
        #         print(parent_title)
        movieDict['RELEASE_YEAR'] = json_object[movieID].get('RELEASE_YEAR')

    return movieDict
