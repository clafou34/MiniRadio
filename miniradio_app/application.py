from radio_config import RadioUiConfig
import bottle
import logging
import os
import sys
from pathlib import Path
from api.radio_api_app import RadioApiApp
from webclient.radio_web_client_app import RadioWebClientApp
from root.radio_root_app import RadioRootApp

# Define absolute path of root
var_path_root = os.path.dirname(os.path.abspath(__file__))

# Get configuration
varConfig = RadioUiConfig(os.path.join(var_path_root, "configuration"))

# Set logging level 
if(varConfig.getRunMode() == "DEBUG"):
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.CRITICAL)

# Create Bottle application
app = bottle.Bottle()

# Initialize API
RadioApiApp.initialize(app, varConfig)

# Initialize WebClient if it is actived
if(varConfig.getUseWebClient()):
    RadioWebClientApp.initialize(app)

# Initialize root page
RadioRootApp.initialize(app, varConfig)

app.run(
    server='gunicorn',
    host=varConfig.getListeningHost(),
    port=varConfig.getListeningPort(),
    keyfile=varConfig.getListeningHttpsKeyFile(),
    certfile=varConfig.getListeningHttpsCertFile(),
    accesslog="-"
          )
