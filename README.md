# Tiny Journeys

Tiny Journeys is a small, travel-themed blog. Not perfect yet, still needs frontend fixes and performance boosting, but at least works to some extend. The aim is to create a simple-looking, but functionable blog service with elements of social networking sites (like Facebook or Instagram). 

By now, a user can:
- create an account, add profile image and log in
- add, edit and delete post and select tag for post (only logged in users)
- add comments to posts (admin can also delete comments)
- like and unlike posts and see who liked posts (only logged in users; user cannot like his own posts)
- see photos for a post in lightbox gallery
- view posts, photos and videos from the whole site with sorting options
- see site statistics
- see own activity statistics (only logged in users)

Features in progress:
- user can see his own and other users' profiles (only logged in users)
- user can see his own activity log
- user can sort posts by Most commented and Most liked
- user can change his account data
- full admin panel 


See (and try!) the blog online: http://jpaliwoda.pythonanywhere.com/

## Built with
- HTML, CSS, JavaScript and [Bootstrap4](https://getbootstrap.com/docs/4.3/getting-started/introduction/) - as a frontend layer
- [Python3.6](https://www.python.org/) - as a backend language
- [Flask](https://palletsprojects.com/p/flask/) - the Python framework
- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) - the Python SQL toolkit
- [Flask-Login](https://flask-login.readthedocs.io/en/latest/) - the library to manage logging sessions
- [Summernote](https://summernote.org/) - an open source, simple WYSIWYG editor
- [Lightbox2](https://lokeshdhakar.com/projects/lightbox2/) - a free-licensed lightbox gallery


## Getting Started
### Clone the repository
    $ git clone https://github.com/asia111307/tiny_journeys.git && cd tiny_journeys

### Run 
#### with Docker
    $ docker-compose up

#### or with virtualenv
You have to install **Python 3.6** on your machine, if you do not have it yet, e.g with: 
    
    $ sudo apt-get install python3.6

Then, install **virtualenv**:

    $ pip install virtualenv 

Create and start **virtual environment**:

    $ virtualenv .env && source .env/bin/activate && pip install -r requirements.txt

Run **project**:

    $ FLASK_APP=start.py FLASK_DEBUG=1 flask run




