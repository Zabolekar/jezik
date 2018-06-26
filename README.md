# jèzik

[![Travis-CI Build Status](https://travis-ci.org/Zabolekar/jezik.svg?branch=master)](https://travis-ci.org/Zabolekar/jezik)

This will be a Serbian dictionary with detailed information about accent.

## Screenshots

![alt text](example.png "Example")

## Requirements

- Python 3.6 or later
- Flask
- PyYAML

We also use pytest to run the tests and mypy for static type checking, but they are not necessary to run the code.

## Running it locally

To run the app locally for development purposes, do the following:

* Clone the repo to a directory named `jezik`
* Create and activate a virtual environment in a way you prefer
* Install the dependencies
```bash
pip install -r requirements.txt
```
* Run the following script (it sets the needed environment variables and starts Flask):
```bash
./run.sh
```
(on Windows cmd, use `run.bat` instead)
* Open [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

## Testing it locally

If the following commands give you errors, don't commit:

* `mypy ../jezik`
* `pytest`

The following commands might give you some useful hints, but don't trust them blindly:

* `pylint ../jezik`
* `flake8`
