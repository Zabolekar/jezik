# jèzik

This will be a Serbian dictionary with detailed information about accent.

## Requirements

- Python 3.6 or later
- Flask
- PyYAML

We also use pytest to run the tests and mypy for static type checking, but they are not necessary to run the code.

## Running it locally

To run the app locally for development purposes, do the following:

* Clone the repo, create and activate a virtual environment in a way you prefer
* Install the dependencies
```bash
pip install -r requirements.txt
```
* Change the working directory to the level where the repo is cloned to (that is, *not* inside the repo directory but directly above)
* Export some Flask-related environment variables
```bash
export FLASK_APP=jezik
export FLASK_ENV=development
```
(on Windows cmd, use `set` instead of `export`)
* Run the app
```bash
flask run
```
* Open [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

## Screenshots

![alt text](example.png "Example")
