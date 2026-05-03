import bottle
from api.utils.radio_playlists import RadioPlaylists
from api.utils.radio_utils import generate_return_dict, remove_url_last_part
from api.utils.radio_queue import RadioQueueManager
from api.utils.radio_player import RadioPlayer
import logging
import traceback
from urllib.parse import urlparse

def setup_routes(app: bottle.Bottle, url_api_root: str, par_obj_radio_playlists: RadioPlaylists, par_obj_radio_queue: RadioQueueManager, par_obj_radio_player: RadioPlayer):
    @app.route(url_api_root + '/playlists', method=['GET'])
    @app.route(url_api_root + '/playlists/', method=['GET'])
    def playlists():
        var_root_dict = {
            "ressources" : [
                {
                    "name" : "Get list of playlist",
                    "uri" : url_api_root + "/playlists/lists/?[type=value]",
                    "url" : bottle.request.url.strip("/") + "/list/",
                    "methods" : "GET",
                    "description" : "Get playlists list. By default, the resource returns all 'playlists'. However, the "
                        + "resource can take a parameter named 'type' which can have 2 values: 'webradio' which allows "
                        + "retrieving only playlists containing internet radios, or 'other' which allows retrieving only playlists "
                        + "that do not contain webradio. "
                },
                {
                    "name" : "Get one playlist detail.",
                    "uri" : url_api_root + "/playlists/<playlist_index:int>/",
                    "methods" : "GET",
                    "description" : "Get playlist which index is supply in uri."
                },
                {
                    "name" : "Get all items in a playlist.",
                    "uri" : url_api_root + "/playlists/<playlist_index:int>/items/",
                    "methods" : "GET",
                    "description" : "Get all items (song or stream) in playlist which index is supply in uri."
                },
                {
                    "name" : "Get an item of a playlist.",
                    "uri" : url_api_root + "/playlists/<playlist_index:int>/items/<item_index_in_playlist:int>",
                    "methods" : "GET, POST",
                    "description" : "Get an item (song or stream) in a playlist which index is supply in uri. "
                        + "If parameter 'action' has 'add-to-queue' value, this ressource allow to Add an item of "
                        + "a playlist at the end of queue. If parameter 'replace' is supplied with value"
                        + "'true', the queue is cleared before adding item. If parammeter 'play' is supplied with value 'true', the player "
                        + "is forced to launch playing."
                },
            ]
        }
        var_return_json = generate_return_dict(True,var_root_dict)
        return var_return_json


    @app.route(url_api_root + '/playlists/list', method=['GET'])
    @app.route(url_api_root + '/playlists/list/', method=['GET'])
    def playlists_root():
        var_return_json = {}
        
        # Récupération du filtre facultatif sur le "type" qui peut avoir la valeur "webradio", "other" ou "all"
        var_selected_type = "all"
        if(bottle.request.query.type == "webradio"):
            var_selected_type = "webradio"
        elif (bottle.request.query.type == "other"):
            var_selected_type = "other"
        
        # Récupération de la racine de l'url
        var_parsed_url = urlparse(bottle.request.url)
        var_base_url = var_parsed_url.scheme + "://" + var_parsed_url.netloc + var_parsed_url.path
        
        try:
            var_lst_obj_playlists = par_obj_radio_playlists.get_playlists(var_selected_type)
            var_playlists_dict=[]
            
            for var_obj_playlist in var_lst_obj_playlists:
                var_playlists_dict.append(
                    {
                        "index" : var_obj_playlist.index,
                        "name" : var_obj_playlist.name,
                        "filename" : var_obj_playlist.filename,
                        "type" : var_obj_playlist.type,
                        "url" : remove_url_last_part(var_base_url) + "/" + str(var_obj_playlist.index)
                        })
            
            var_return_json = generate_return_dict(True,{"playlists_type" : var_selected_type, "playlists" : var_playlists_dict})
            
        except Exception as e:
            var_error_message = "Error when getting all playlists."
            logging.error(f"{var_error_message} : {traceback.format_exc()}")
            bottle.abort(500,var_error_message)
        
        return var_return_json

    @app.route(url_api_root + '/playlists/<playlist_index:int>', method=['GET'])
    @app.route(url_api_root + '/playlists/<playlist_index:int>/', method=['GET'])
    def playlist(playlist_index):
        var_return_json = {}
        
        try:
            var_obj_playlist = par_obj_radio_playlists.get_playlist(playlist_index)
            if var_obj_playlist is None:
                var_return_json = None
            else:
                var_playlist_dict={"index" : var_obj_playlist.index,
                                        "name" : var_obj_playlist.name,
                                        "filename" : var_obj_playlist.filename,
                                        "type" : var_obj_playlist.type,
                                        "items_url" : bottle.request.url.strip("/") + "/items"
                                        }
            
                var_return_json = generate_return_dict(True,{"playlist" : var_playlist_dict})
        except Exception as e:
            var_error_message = f"Error when getting stored playlists '{str(playlist_index)}'."
            logging.error(f"{var_error_message} : {traceback.format_exc()}")
            bottle.abort(500,var_error_message)
        
        if var_return_json is None:
            bottle.abort(404)
        
        return var_return_json


    @app.route(url_api_root + '/playlists/<playlist_index:int>/items', method=['GET'])
    @app.route(url_api_root + '/playlists/<playlist_index:int>/items/', method=['GET'])
    def playlist_items(playlist_index):
        var_return_json = {}
        
        try:
            var_obj_item_list = par_obj_radio_playlists.get_items(playlist_index)
            if var_obj_item_list is None:
                var_return_json = None
            else:
                var_items_dict=[]
                var_index_in_playlist = 0
                for var_obj_item in var_obj_item_list:
                    var_item_url = bottle.request.url.strip("/") + "/" + str(var_index_in_playlist)
                    var_items_dict.append({ "index" : var_index_in_playlist,
                                            "item" : {
                                                "file" : var_obj_item.file,
                                                "name" : var_obj_item.name,
                                                "title" : var_obj_item.title,
                                                "album" : var_obj_item.album,
                                                "artist" : var_obj_item.artist,
                                                "date" : var_obj_item.date,
                                                "genre" : var_obj_item.genre,
                                                "mr_stream_name" : var_obj_item.mr_stream_name,
                                                "mr_playlist_index" : var_obj_item.mr_playlist_index,
                                                "mr_playlist_name" : var_obj_item.mr_playlist_name,
                                                "item_url" : var_item_url,
                                                "item_url_to_add_in_queue" : var_item_url + "?action=add-to-queue",
                                                "item_url_to_replace_in_queue" : var_item_url + "?action=add-to-queue&replace=true",
                                                "item_url_to_replace_and_play" : var_item_url + "?action=add-to-queue&replace=true&play=true",
                                                }
                                            })
                    var_index_in_playlist = var_index_in_playlist + 1
            
                var_return_json = generate_return_dict(True,{"items" : var_items_dict})
        except Exception as e:
            var_error_message = f"Error when getting items of stored playlists '{str(playlist_index)}'."
            logging.error(f"{var_error_message} : {traceback.format_exc()}")
            bottle.abort(500,var_error_message)
        
        if var_return_json is None:
            bottle.abort(404)
        
        return var_return_json
    
    @app.route(url_api_root + '/playlists/<playlist_index:int>/items/<item_index_in_playlist:int>', method=['GET','POST'])
    @app.route(url_api_root + '/playlists/<playlist_index:int>/items/<item_index_in_playlist:int>/', method=['GET','POST'])
    def playlist_item(playlist_index, item_index_in_playlist):
        var_return_json = {}

        # Get parameter for replacing queue content by item
        var_bool_replace_queue = False
        var_param_replace = bottle.request.params.get("replace")
        if(var_param_replace is not None):
            if(var_param_replace == "true"):
                var_bool_replace_queue = True
        
        # Get parameter to force playing
        var_bool_play = False
        var_param_play = bottle.request.params.get("play")
        if(var_param_play is not None):
            if(var_param_play == "true"):
                var_bool_play = True
        
        # Get parameter for add to queue action
        var_bool_add_action = False
        var_param_add = bottle.request.params.get("action")
        if(var_param_add is not None):
            if(var_param_add == "add-to-queue"):
                var_bool_add_action = True
        
        if var_bool_add_action:
            try:
                var_item = par_obj_radio_playlists.get_item(playlist_index, item_index_in_playlist)
                if var_item is not None:
                    if var_bool_replace_queue :
                        par_obj_radio_queue.clear()
                    par_obj_radio_queue.add_radio_item(var_item)
                    if var_bool_play:
                        par_obj_radio_player.play()
                    var_return_json = generate_return_dict(True)
            except Exception as e:
                var_error_message = f"Error when adding item of stored playlist to queue."
                logging.error(f"{var_error_message} : {traceback.format_exc()}")
                bottle.abort(500,var_error_message)
        else:
            var_obj_item = par_obj_radio_playlists.get_item(playlist_index,item_index_in_playlist)
            if var_obj_item is None:
                var_return_json = None
            else:
                try:
                    var_item_url = bottle.request.url.strip("/")
                    var_item_dict = {
                                        "file" : var_obj_item.file,
                                        "name" : var_obj_item.name,
                                        "title" : var_obj_item.title,
                                        "album" : var_obj_item.album,
                                        "artist" : var_obj_item.artist,
                                        "mr_stream_name" : var_obj_item.mr_stream_name,
                                        "mr_playlist_index" : var_obj_item.mr_playlist_index,
                                        "mr_playlist_name" : var_obj_item.mr_playlist_name,
                                        "item_url" : var_item_url,
                                        "item_url_to_add_in_queue" : var_item_url + "?action=add-to-queue",
                                        "item_url_to_replace_in_queue" : var_item_url + "?action=add-to-queue&replace=true",
                                        "item_url_to_replace_and_play" : var_item_url + "?action=add-to-queue&replace=true&play=true",
                                    }
                
                    var_return_json = generate_return_dict(True,{"item" : var_item_dict})
                except Exception as e:
                    var_error_message = f"Error when getting item of stored playlists '{str(playlist_index)}'."
                    logging.error(f"{var_error_message} : {traceback.format_exc()}")
                    bottle.abort(500,var_error_message)
        
        if var_return_json is None:
            bottle.abort(404)
        
        return var_return_json
