# jèzik

This will be a Serbian dictionary with detailed information about accent.

## Requirements

- Python 3.6 or later
- Flask
- PyYAML

Steps to get it work locally:

* Create and activate a virtual environment in a way you prefer
* Install the dependencies
```bash
pip install -r requirements.txt
```
* Export some Flask-related environment variables
```bash
export FLASK_APP=jezik
export FLASK_ENV=development
```
(on Windows cmd, use `set` instead of `export`)
* Change the working directory to the level where the repo is cloned to (that is, *not* inside the repo directory)
* Run flask application
```bash
flask run
```

![alt text](example.png "Example")
