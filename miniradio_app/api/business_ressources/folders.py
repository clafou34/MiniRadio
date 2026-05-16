import bottle
import logging
import os
import traceback
from api.utils.radio_folders import RadioFolders, RadioFoldersNoExistError
from api.utils.radio_queue import RadioQueueManager
from api.utils.radio_utils import RadioUtils
from api.utils.radio_player import RadioPlayer
from urllib.parse import urlparse

def setup_routes(app: bottle.Bottle, url_api_root: str, par_obj_radio_folders: RadioFolders, par_obj_radio_queue: RadioQueueManager, par_obj_radio_player: RadioPlayer):

    @app.route(url_api_root + '/folders', method=['GET'])
    @app.route(url_api_root + '/folders/', method=['GET'])
    @app.route(url_api_root + '/folders/<folder_path:path>', method=['GET'])
    @app.route(url_api_root + '/folders/<folder_path:path>/', method=['GET'])
    def content(folder_path:str = ''):
        var_return_json = {}

        # Control string security
        if("//" in folder_path) or (".." in folder_path) or folder_path.startswith("/"):
            var_error_message = "Path string is incorrect"
            bottle.abort(403,var_error_message)            

        try:
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

            # Obtain the content from the URL provided as a parameter.
            var_folder_content = par_obj_radio_folders.get_content(folder_path)

        except RadioFoldersNoExistError as e:
            var_error_message = "Error when getting folders."
            logging.error(f"{var_error_message} : {traceback.format_exc()}")
            bottle.abort(404,var_error_message)           
        except Exception as e:
            var_error_message = "Error when getting folders."
            logging.error(f"{var_error_message} : {traceback.format_exc()}")
            bottle.abort(500,var_error_message)

        if var_bool_add_action :    # Adding items
            try:
                if var_bool_replace_queue :
                    par_obj_radio_queue.clear()

                for var_obj_item in var_folder_content.items:
                    par_obj_radio_queue.add_radio_item(var_obj_item)

                if var_bool_play:
                    par_obj_radio_player.play()
                
                var_return_json = RadioUtils.generate_return_dict(True)
            except Exception as e:
                var_error_message = "Error when adding folder content to queue."
                logging.error(f"{var_error_message} : {traceback.format_exc()}")
                bottle.abort(500,var_error_message)
        else:   #Getting items
            try:
                # Check if request one file, or a folder
                var_bol_one_file = False
                if len(var_folder_content.folders)==0 and len(var_folder_content.items)==1:
                    var_bol_one_file = True

                var_folders_dict = []
                for var_obj_folder in var_folder_content.folders:
                    var_folder_url = bottle.request.url.strip("/") + "/" + var_obj_folder.name.split('/')[-1]
                    var_folders_dict.append({ "name" : var_obj_folder.name,
                                            "path" : var_obj_folder.path,
                                            "url" : var_folder_url,
                                            "url_to_add_in_queue" : var_folder_url + "?action=add-to-queue",
                                            "url_to_replace_in_queue" : var_folder_url + "?action=add-to-queue&replace=true",
                                            "url_to_replace_and_play" : var_folder_url + "?action=add-to-queue&replace=true&play=true",
                                            })

                var_items_dict = []
                for var_obj_item in var_folder_content.items:
                    var_item_url = bottle.request.url.split("?")[0] if var_bol_one_file else bottle.request.url.strip("/") + "/" + var_obj_item.file.split('/')[-1]
                    var_items_dict.append({     "file" : var_obj_item.file,
                                                "name" : var_obj_item.name,
                                                "title" : var_obj_item.title,
                                                "album" : var_obj_item.album,
                                                "artist" : var_obj_item.artist,
                                                "date" : var_obj_item.date,
                                                "genre" : var_obj_item.genre,
                                                "mr_stream_name" : var_obj_item.mr_stream_name,
                                                "mr_playlist_index" : var_obj_item.mr_playlist_index,
                                                "mr_playlist_name" : var_obj_item.mr_playlist_name,
                                                "url" : var_item_url,
                                                "url_to_add_in_queue" : var_item_url + "?action=add-to-queue",
                                                "url_to_replace_in_queue" : var_item_url + "?action=add-to-queue&replace=true",
                                                "url_to_replace_and_play" : var_item_url + "?action=add-to-queue&replace=true&play=true",
                                            })

                var_return_json = var_return_json = RadioUtils.generate_return_dict(True, {"folders" : var_folders_dict, "items" : var_items_dict})
            except Exception as e:
                var_error_message = "Error when getting folders."
                logging.error(f"{var_error_message} : {traceback.format_exc()}")
                bottle.abort(500,var_error_message)

        return var_return_json