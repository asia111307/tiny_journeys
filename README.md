# tiny_journeys
A small blog written in Flask. Not perfect yet, still needs Frontend fixes and performance boosting, but at least works to some extend

See the blog online: http://jpaliwoda.pythonanywhere.com/

## How to run the project locally:
### Create and start virtual environment
$ virtualenv .env && source .env/bin/activate && pip install -r requirements.txt

### Install node modules
$ npm install

### Run gulp
$ gulp watch

### Run project
$ FLASK_APP=start.py FLASK_DEBUG=1 flask run
