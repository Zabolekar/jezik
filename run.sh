#!/bin/bash
export FLASK_APP=../jezik
export FLASK_ENV=development
flask run --cert=cert.pem --key=key.pem