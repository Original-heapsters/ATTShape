import os
import json
import config
from shutil import copyfile
from flask import Flask, render_template, request, url_for, redirect
from werkzeug.utils import secure_filename

app = Flask(__name__)

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
