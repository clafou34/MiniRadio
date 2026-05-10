import traceback
import logging
import bottle
import json
from api.utils.radio_utils import generate_return_dict
from api.utils.radio_connection import RadioConnection
from urllib.parse import urljoin


def setup_routes(app: bottle.Bottle, url_api_root: str, par_obj_radio_connection: RadioConnection, run_mode: str):

    @app.route(url_api_root + '/', method=['GET'])
    @app.route(url_api_root, method=['GET'])
    def api_root():
        var_root_dict = {
            "ressources" : [
                {
                    "name" : "Player",
                    "uri" : url_api_root + "/player/",
                    "url" : bottle.request.url.strip("/") + "/player/",
                    "methods" : "GET",
                    "description" : "Control music player."
                },
                {
                    "name" : "Queue",
                    "uri" : url_api_root + "/queue/",
                    "url" : bottle.request.url.strip("/") + "/queue/",
                    "methods" : "GET",
                    "description" : "Manage queue."
                },
                {
                    "name" : "Playlists",
                    "uri" : url_api_root + "/playlists/",
                    "url" : bottle.request.url.strip("/") + "/playlists/",
                    "methods" : "GET",
                    "description" : "Manage stored playlists."
                },
                {
                    "name" : "Folders",
                    "uri" : url_api_root + "/folders/",
                    "url" : bottle.request.url.strip("/") + "/folders/",
                    "methods" : "GET",
                    "description" : "View and play music in mpd folders."
                },
                {
                    "name" : "System settings",
                    "uri" : url_api_root + "/settings/",
                    "url" : bottle.request.url.strip("/") + "/settings/",
                    "methods" : "GET",
                    "description" : "Allow to manipulate system settings."
                },
            ]
        }
        var_return_json = generate_return_dict(True,var_root_dict)
        
        return var_return_json

    # Set code to execute before all requests
    @app.hook('before_request')
    def setup_before_request():
        # Manage connexion only for API ressources
        if (url_api_root in bottle.request.urlparts.path):
            # If connexion is not done, connect to MPD server
            try:
                par_obj_radio_connection.check_connection()
            except Exception as e:
                    var_error_message = "Error at connection."
                    logging.error(f"{var_error_message} : {traceback.format_exc()}")
                    bottle.abort(500,var_error_message)
        

    # Middleware pour ajouter des en-têtes de cache
    @app.hook('after_request')
    def setup_after_request():
        # Desactivate cache in debug mode.
        if(run_mode == "DEBUG"):
            bottle.response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            bottle.response.headers['Pragma'] = 'no-cache'
            bottle.response.headers['Expires'] = '0'

    @app.error(404)
    def error_404_handler(obj_error):
        bottle.response.content_type = 'application/json'
        content_json = {
            "http_code" : str(obj_error.status_code),
            "http_error" : "Not found",
        }
        return json.dumps(content_json)
    
    @app.error(500)
    def error_500_handler(obj_error):
        bottle.response.content_type = 'application/json'
        content_text = "{"
        content_text = content_text + "\"http_code\" : \"" + str(obj_error.status_code) + "\","
        content_text = content_text + "\"http_error\" : \"Internal Server Error\","
        content_text = content_text + "\"message\" : \"" + obj_error.body + "\""
        content_text = content_text + "}"
        return content_text