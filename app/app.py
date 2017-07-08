import os
import json
import config
from shutil import copyfile
from flask import Flask, render_template, request, url_for, redirect
from werkzeug.utils import secure_filename

app = Flask(__name__)


#######################################
# Constants
#######################################
ASSETS = 'static/Assets/'
DATA_FILE = ASSETS + 'runningData.txt'
RESULTS_FILE = ASSETS + 'finalPrediction.txt'
LOG_FILE = ASSETS + 'ATTSHAPE.log'
ENDPOINTS = ['index','Browse','Select', 'Back', 'Done']

#######################################
# Setup
#######################################
if os.path.isdir(ASSETS) is False:
    os.makedirs(ASSETS)

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
        return render_template('index.html')
    else:
        log('Index GET')
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
