# jèzik

This will be a Serbian dictionary with detailed information about accent.

## Requirements

- Python 3.6 or later
- Flask
- PyYAML

Steps to get it work locally:

* Install virtualenv 
```bash
mkvirtualenv -p pytyhon3.6 jezik
```
* Install dependencies
```bash
pip install -r requirements.txt
```
* To make it work as a flask app
```bash
export FLASK_APP=jezik
export FLASK_ENV=development
```

* Change directory to the level where the repo is cloned to (do not enter inside the repo directory)

* Run flask application
```bash
flask run
```

![alt text](example.png "Example")
