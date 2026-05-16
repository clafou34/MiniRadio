import bottle
import logging
import traceback
from api.utils.radio_settings import RadioSettings
from api.utils.radio_playlists import RadioPlaylists
from api.utils.radio_utils import RadioUtils

def setup_routes(app: bottle.Bottle, url_api_root: str, par_obj_radio_settings: RadioSettings, par_obj_radio_playlists: RadioPlaylists ):

    @app.route(url_api_root + '/settings', method=['GET','POST'])
    @app.route(url_api_root + '/settings/', method=['GET','POST'])
    def config_root():
        posted_data = bottle.request.json
        if(posted_data is None):
            posted_data = {}

        # Get parameter action
        var_action = ""
        if("action" in posted_data):
            var_action = posted_data.get('action')
        else:
            var_param_action = bottle.request.params.get("action")
            if(var_param_action is not None):
                var_action = var_param_action

        # If action is "refresh-db"
        if var_action == "refresh-db":
            try:
                par_obj_radio_settings.refresh_db()
                par_obj_radio_playlists.load_playlist()
                var_return_json = RadioUtils.generate_return_dict(True)
            except Exception as e:
                var_error_message = "Error when refreshing database with filesystem changes."
                logging.error(f"{var_error_message} : {traceback.format_exc()}")
                bottle.abort(500,var_error_message)

        # If there is no action or an invalid action, then show help
        else:
            var_root_dict = {
                "ressources" : [
                    {
                        "name" : "System settings manipulation",
                        "uri" : url_api_root + "/settings",
                        "url" : bottle.request.url.strip("/"),
                        "methods" : "GET, POST",
                        "description" : "Allow to manipulate system settings. The main parameter is 'action'. action=refresh-db ==>  Refresh the database with the filesystem changes.",
                        "url_to_refresh_db" : bottle.request.url.strip("/") + "?action=refresh-db",
                    },
                ]
            }
            var_return_json = RadioUtils.generate_return_dict(True,var_root_dict)

        return var_return_json


