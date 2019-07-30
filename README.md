# Tiny Journeys

Tiny Journeys is a small, travel-themed blog. Not perfect yet, still needs frontend fixes and performance boosting, but at least works to some extend. The aim is to create a simple-looking, but functionable blog service with elements of social networking sites (like Facebook or Instagram). 

By now, a user can:
- create an account and login
- add, edit and delete post and select tag for post (only logged in users)
- add comments to posts (admin can also delete comments)
- like and unlike posts and see who liked posts (only logged in users)
- see photos for a post in lightbox gallery
- view posts, photos and videos from the whole site with sorting options
- see site statistics
- see own activity statistics (only logged in users)

Features in progress:
- user can see his own and other users' profiles (only logged in users)
- user can see his own activity log
- full admin panel 

See (and try!) the blog online: http://jpaliwoda.pythonanywhere.com/

## Build with
- HTML, CSS and JavsScript - as a frontend layer
- [Python3.6](https://www.python.org/) - as a backend language
- [Flask](https://palletsprojects.com/p/flask/) - the Python framework
- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) - the Python SQL toolkit
- [Flask-Login](https://flask-login.readthedocs.io/en/latest/) - the library to manage logging sessions
- [Summernote](https://summernote.org/) - an open source, simple WYSIWYG editor
- [Lightbox2](https://lokeshdhakar.com/projects/lightbox2/) - a free-licensed plugin for lightbox gallery


## Getting Started

You have to install **Python 3.6** on your machine, if you do not have it yet, e.g with: 
    
    $ sudo apt-get install python3.6

Then, install **virtualenv**:

    $ pip install virtualenv 


You also have to install **NodeJS**, if you do not have it yet, e.g with: 

    $ sudo apt-get install nodejs

Then, install **npm**:

    $ sudo apt-get install npm

### Clone the repository
    $ git clone https://github.com/asia111307/tiny_journeys.git && cd tiny_journeys

### Create and start virtual environment
    $ virtualenv .env && source .env/bin/activate && pip install -r requirements.txt

### Run gulp
    $ npm install
    $ gulp watch

### Run project
    $ FLASK_APP=start.py FLASK_DEBUG=1 flask run
