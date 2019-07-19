# tiny_journeys
A small blog written in Flask. Not perfect yet, still needs Frontend fixes and performance boosting, but at least works to some extend

See the blog online: http://jpaliwoda.pythonanywhere.com/

## How to run the project locally:
You have to install Python 3.6 on your machine, if you do not have it yet (e.g with $ sudo apt-get install python3.6).

Then, install virtualenv

$ pip install virtualenv 


You also have to install NodeJS, if you do not have it yet(e.g with $ sudo apt-get install nodejs)

Then, install npm

$ sudo apt-get install npm

### Clone the repository
$ git clone https://github.com/asia111307/tiny_journeys.git && cd tiny_journeys

### Create and start virtual environment
$ virtualenv .env && source .env/bin/activate && pip install -r requirements.txt

### Install node modules
$ npm install

### Run gulp
$ gulp watch

### Run project
$ FLASK_APP=start.py FLASK_DEBUG=1 flask run
