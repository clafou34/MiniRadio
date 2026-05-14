#
# For running this project, you need to launch theses 2 commands in your environnement
#   pip install bottle
#   pip install python-mpd2
#

from webclient import web_client
from radio_config import RadioUiConfig
import bottle
import logging
import os
from pathlib import Path
from api.business_ressources import player, utils, playlists, queue, folders, settings
from api.utils.radio_connection import RadioConnection
from api.utils.radio_playlists import RadioPlaylists
from api.utils.radio_folders import RadioFolders
from api.utils.radio_player import RadioPlayer
from api.utils.radio_queue import RadioQueueManager
from api.utils.radio_settings import RadioSettings
from api.utils.radio_item_display_manager import ItemDisplayManager




#logging.basicConfig(level=logging.DEBUG)

# Define url roots for API et Web Client
var_url_root_api = "/api"
var_url_root_web_client = "/webclient"

# Define absolute path of root
var_path_root = os.path.dirname(os.path.abspath(__file__))

# Create application Bottle
app = bottle.Bottle()

# Get configuration
varConfig = RadioUiConfig(os.path.join(var_path_root, "configuration"))

# Set logging level 
if(varConfig.getRunMode() == "DEBUG"):
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.CRITICAL)

# Get radio player connection
var_radio_connexion = RadioConnection(varConfig.getMpdAddress(), varConfig.getMpdPort())
var_radio_connexion.check_connection()

# Get items display manager
var_obj_item_display_manager = ItemDisplayManager()

# Get player manager
var_obj_radio_player = RadioPlayer(var_radio_connexion)

# Get Queue manager
var_obj_radio_queue = RadioQueueManager(var_radio_connexion, var_obj_item_display_manager)

# Get playlists manager
var_obj_radio_playlists = RadioPlaylists(var_radio_connexion, var_obj_item_display_manager, varConfig)

# Get folders manager
var_obj_radio_folders = RadioFolders(var_radio_connexion, var_obj_item_display_manager)

# Get config manager
var_obj_radio_settings = RadioSettings(var_radio_connexion)

# Set routes
player.setup_routes(app, var_url_root_api, var_obj_radio_player, var_obj_radio_queue)
playlists.setup_routes(app, var_url_root_api, var_obj_radio_playlists, var_obj_radio_queue, var_obj_radio_player)
folders.setup_routes(app, var_url_root_api, var_obj_radio_folders, var_obj_radio_queue, var_obj_radio_player)
queue.setup_routes(app, var_url_root_api, var_obj_radio_queue)
settings.setup_routes(app, var_url_root_api, var_obj_radio_settings, var_obj_radio_playlists)
utils.setup_routes(app, var_url_root_api, var_radio_connexion, varConfig.getRunMode())
if(varConfig.getUseWebClient()):
    web_client.setup_routes(app, var_path_root, var_url_root_web_client, var_url_root_api)

@app.route('/')
@app.route('/index.html')
def root_uri():
    try:
        var_index_path = Path(os.path.join(var_path_root, "index.html"))
    
        with open(var_index_path, 'r', encoding='utf-8') as index_file:
            var_content = index_file.read()
        
    except Exception as e:
        bottle.abort(404)
        
    return bottle.template(var_content, 
        url_web_client = var_url_root_web_client if varConfig.getUseWebClient() else "",
        url_api = var_url_root_api
        )

app.run(host='0.0.0.0', port=varConfig.getListeningPort())
