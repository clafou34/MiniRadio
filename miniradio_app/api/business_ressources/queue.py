import bottle
from api.utils.radio_queue import RadioQueueManager, RadioQueueNotFoundError
from api.utils.radio_utils import RadioUtils
import logging
import traceback

def setup_routes(app: bottle.Bottle, url_api_root: str, par_obj_radio_queue: RadioQueueManager):

    @app.route(url_api_root + '/queue')
    @app.route(url_api_root + '/queue/')
    def queue_root():
        var_root_dict = {
            "ressources" : [
                {
                    "name" : "Get or manage list of items in queue",
                    "uri" : url_api_root + "/queue/items",
                    "url" : bottle.request.url.strip("/") + "/items",
                    "url_to_clear_queue" : bottle.request.url.strip("/") + "/items?action=clear",
                    "methods" : "GET",
                    "description" : "If 'action' parameter is empty, get all items in queue. If 'action' parameter has 'clear' value then queue is cleared."
                },
                {
                    "name" : "Get an item in queue",
                    "uri" : url_api_root + "/queue/items/<item_id>",
                    "url" : bottle.request.url.strip("/") + "/items",
                    "methods" : "GET",
                    "description" : "Get item from queue with his id."
                },
                {
                    "name" : "Delete an item in queue",
                    "uri" : url_api_root + "/queue/items/<item_id>",
                    "url" : bottle.request.url.strip("/") + "/items",
                    "methods" : "DELETE",
                    "description" : "Delete item from queue with his id."
                },
            ]
        }
        var_return_json = RadioUtils.generate_return_dict(True,var_root_dict)
        return var_return_json

    
    @app.route(url_api_root + '/queue/items', method=['GET'])
    @app.route(url_api_root + '/queue/items/', method=['GET'])
    def items():
        var_return_json = {}
        
        # Get parameter for clearig queue
        var_bool_clear_queue = False
        var_param_clear_queue = bottle.request.params.get("action")
        if(var_param_clear_queue is not None):
            if(var_param_clear_queue == "clear"):
                var_bool_clear_queue = True

        if not var_bool_clear_queue :
            try:
                var_obj_queue_item_list = par_obj_radio_queue.get_items()
                if var_obj_queue_item_list is None:
                    var_return_json = None
                else:
                    var_items_dict=[]
                    for var_obj_queue_item in var_obj_queue_item_list:
                        var_items_dict.append({
                            "id" : var_obj_queue_item.id,
                            "pos" : var_obj_queue_item.pos,
                            "queued_item" : { "file" : var_obj_queue_item.queued_item.file,
                                                "name" : var_obj_queue_item.queued_item.name,
                                                "title" : var_obj_queue_item.queued_item.title,
                                                "album" : var_obj_queue_item.queued_item.album,
                                                "artist" : var_obj_queue_item.queued_item.artist,
                                                "date" : var_obj_queue_item.queued_item.date,
                                                "genre" : var_obj_queue_item.queued_item.genre,
                                                "mr_stream_name" : var_obj_queue_item.queued_item.mr_stream_name,
                                                "mr_playlist_index" : var_obj_queue_item.queued_item.mr_playlist_index,
                                                "mr_playlist_name" : var_obj_queue_item.queued_item.mr_playlist_name
                                                }})
                
                    var_return_json = RadioUtils.generate_return_dict(True,{"items" : var_items_dict})
            except Exception as e:
                var_error_message = f"Error when getting items of queue'."
                logging.error(f"{var_error_message} : {traceback.format_exc()}")
                bottle.abort(500,var_error_message)
        else:
            try:
                par_obj_radio_queue.clear()
                var_return_json = RadioUtils.generate_return_dict(True)
            except Exception as e:
                var_error_message = f"Error when clearing queue'."
                logging.error(f"{var_error_message} : {traceback.format_exc()}")
                bottle.abort(500,var_error_message)

        
        if var_return_json is None:
            bottle.abort(404)
        
        return var_return_json

    @app.route(url_api_root + '/queue/items/<item_id:int>', method=['GET'])
    @app.route(url_api_root + '/queue/items/<item_id:int>/', method=['GET'])
    def get_item(item_id:int):
        var_return_json = {}
        
        try:
            var_obj_queue_item = par_obj_radio_queue.get_item(item_id)
            
            var_item_dict = {
                        "id" : var_obj_queue_item.id,
                        "pos" : var_obj_queue_item.pos,
                        "queued_item" : { "file" : var_obj_queue_item.queued_item.file,
                                            "name" : var_obj_queue_item.queued_item.name,
                                            "title" : var_obj_queue_item.queued_item.title,
                                            "album" : var_obj_queue_item.queued_item.album,
                                            "artist" : var_obj_queue_item.queued_item.artist,
                                            "date" : var_obj_queue_item.queued_item.date,
                                            "genre" : var_obj_queue_item.queued_item.genre,
                                            "mr_stream_name" : var_obj_queue_item.queued_item.mr_stream_name,
                                            "mr_playlist_index" : var_obj_queue_item.queued_item.mr_playlist_index,
                                            "mr_playlist_name" : var_obj_queue_item.queued_item.mr_playlist_name
                                            }}
            
            var_return_json = RadioUtils.generate_return_dict(True, {"item" : var_item_dict})
        except RadioQueueNotFoundError:
            bottle.abort(404)
        except Exception as e:
            var_error_message = f"Error when deleting item from queue'."
            logging.error(f"{var_error_message} : {traceback.format_exc()}")
            bottle.abort(500,var_error_message)
        
        return var_return_json

    @app.route(url_api_root + '/queue/items/<item_id:int>', method=['DELETE'])
    @app.route(url_api_root + '/queue/items/<item_id:int>/', method=['DELETE'])
    def delete_item(item_id:int):
        var_return_json = {}
        
        try:
            par_obj_radio_queue.delete_item(item_id)
            
            var_return_json = RadioUtils.generate_return_dict(True)
        except RadioQueueNotFoundError:
            bottle.abort(404)
        except Exception as e:
            var_error_message = f"Error when deleting item from queue'."
            logging.error(f"{var_error_message} : {traceback.format_exc()}")
            bottle.abort(500,var_error_message)
        
        return var_return_json