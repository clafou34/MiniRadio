from radio_config import RadioUiConfig
import bottle
import logging
import os
from pathlib import Path
from api.radio_api_app import RadioApiApp
from webclient.radio_web_client_app import RadioWebClientApp
from root.radio_root_app import RadioRootApp

# Define absolute path of root
var_path_root = os.path.dirname(os.path.abspath(__file__))

# Create Bottle application
app = bottle.Bottle()

# Get configuration
varConfig = RadioUiConfig(os.path.join(var_path_root, "configuration"))

# Set logging level 
if(varConfig.getRunMode() == "DEBUG"):
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.CRITICAL)


# Initialize API
RadioApiApp.initialize(app, varConfig)

# Initialize WebClient if it is actived
if(varConfig.getUseWebClient()):
    RadioWebClientApp.initialize(app)

# Initialize root page
RadioRootApp.initialize(app, varConfig)

app.run(host='0.0.0.0', port=varConfig.getListeningPort())
