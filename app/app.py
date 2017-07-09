import os
import shutil
import json
import config
import MovieParser as movParse
import trailerOps as trailer
from shutil import copyfile
from flask import Flask, render_template, request, url_for, redirect
from werkzeug.utils import secure_filename

app = Flask(__name__)


#######################################
# Constants
#######################################
ASSETS = 'static/Assets/'
POSTERS = ASSETS + 'images/Posters/'
TRAILERS = ASSETS + 'videos/Trailers/'
USER_FILE = ASSETS + 'UserData.txt'
RESULTS_FILE = ASSETS + 'finalSuggestion.txt'
LOG_FILE = ASSETS + 'ATTSHAPE.log'
ENDPOINTS = ['index','Browse','Select', 'Back', 'Done']

#######################################
# Setup
#######################################
if os.path.isdir(ASSETS) is False:
    os.makedirs(ASSETS)

if os.path.isdir(POSTERS) is False:
    os.makedirs(POSTERS)
else:
    shutil.rmtree(POSTERS)
    os.makedirs(POSTERS)

if os.path.isdir(TRAILERS) is False:
    os.makedirs(TRAILERS)
else:
    shutil.rmtree(TRAILERS)
    os.makedirs(TRAILERS)

#######################################
# Routing
#######################################
@app.route('/', methods=['GET','POST'])
def index():
    '''
    GET
        Display some sort of dashboard
    POST
        unused
    '''
    if request.method == 'POST':
        log('Index POST')
        uName = request.form['UserName']

        ChosenGenres = []
        MovieDict = {}
        Movies = []
        Posters = []
        TrailerURLS = []

        if config.ConfigVars['MockForFE'] == 1:
            ChosenGenres = ['Horror','Comedy','War', 'Western']
            ChosenMovies = ['urn:dece:cid:eidr-s:EDA7-D64D-A836-9630-677A-1']#,'urn:dece:cid:eidr-s:360F-8376-C1AE-A473-42FC-F','urn:dece:cid:org:WB:2044719x600004920501','urn:dece:cid:eidr-s:9BE6-6378-4139-C64E-3BE7-8']
        else:
            ChosenGenres = AnalyzePersonality(uName)
            ChosenMovies = GetRelevantMovies(ChosenGenres)

        for mov in ChosenMovies:
            log('Getting movie data for ' + mov)
            MovieDict = movParse.GetMovieInfo(mov)
            Movies.append(MovieDict)
            trailer.DownloadPosters(MovieDict.get('POSTER_URL'),POSTERS,mov)
            urlList = trailer.GetYoutubeURLS('Warner bros trailer ' + MovieDict.get('CONTENT_TITLE'))
            trailer.DownloadTrailer(urlList,TRAILERS,mov)
            TrailerURLS.append(urlList)
            Posters.append(mov)
            log(str(Movies))

        return render_template('Browse.html',UserName=uName, ChosenGenres=ChosenGenres, ChosenMovies=ChosenMovies, Movies=Movies, Posters=Posters)
    else:
        log('Index GET')
        log('Clearing dir '+ POSTERS)
        shutil.rmtree(POSTERS)
        os.makedirs(POSTERS)
        shutil.rmtree(TRAILERS)
        os.makedirs(TRAILERS)
        return render_template('index.html')

@app.route('/Back', methods=['GET','POST'])
def Back():
    '''
    GET
        Back track one step
    '''
    log('Back GET')
    return render_template('Back.html')

@app.route('/Browse', methods=['GET','POST'])
def Browse():
    '''
    GET
        Display visually appealing intro environment
    '''
    log('Browse GET')
    return render_template('Browse.html')

@app.route('/Done', methods=['GET','POST'])
def Done():
    '''
    GET
        Go to done page
    '''
    log('Done GET')
    return render_template('Done.html')

@app.route('/Select', methods=['GET','POST'])
def Select():
    '''
    GET
        Alter three.js environment based on suggestion results
    '''
    log('Select GET')
    return render_template('Select.html')

@app.route('/City', methods=['GET','POST'])
def City():
    '''
    GET
        Alter three.js environment based on suggestion results
    '''
    log('City GET')
    return render_template('city.html')

def log(text):
    text = str(text)
    if config.ConfigVars['LogLevel'] == 0:
        return True

    if config.ConfigVars['LogLevel'] == 3:
        with open(LOG_FILE, 'a') as logger:
            logger.write(text)
            logger.close()
        print(text)
        return True

    if config.ConfigVars['LogLevel'] == 2:
        print(text)

    if config.ConfigVars['LogLevel'] == 1:
        with open(LOG_FILE, 'a') as logger:
            logger.write(text)
            logger.close()

#######################################
# Running
#######################################
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
