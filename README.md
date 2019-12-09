# jèzik

[![Travis-CI Build Status](https://travis-ci.org/Zabolekar/jezik.svg?branch=master)](https://travis-ci.org/Zabolekar/jezik)

This will be a Serbian dictionary with detailed information about accent.

## Screenshots

![Example screenshot](example.png "Example")

## Requirements

* Python 3.7 or later
* Flask
* PyYAML

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
* Open <http://127.0.0.1:5000/>

## Using it without the web interface

You can use the underlying `lookup` function directly. It returns `Multitable` objects that can be queried in a flexible manner:

```python
>>> lookup("ауторски")["nom sg"]
 [nom sg]
m sg nom            а̀уторскӣ
f sg nom            а̀уторска̄
n sg nom            а̀уторско̄
```

However, the output may be incorrect depending on your console font. We've found Noto Mono and Fira Code to work well.

## Testing it locally

If the following commands give you errors, don't commit:

* `mypy ../jezik`
* `pytest`

The following commands might give you some useful hints, but don't trust them blindly:

* `pylint ../jezik`
* `flake8`

We also have configured `pytest --quick` to skip the most time-consuming tests but still perform the quick ones; this is useful during development.
