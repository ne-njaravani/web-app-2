#!/bin/bash

source flask/bin/activate
cd Social_media_site/

# Try to run the Flask application on the default port
if ! flask run; then
    # If the above command fails, run it on port 4444
    flask run --port 4444
fi