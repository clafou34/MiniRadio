import bottle
from api.utils.radio_player import RadioPlayer, RadioPlayerBadSongIdError
from api.utils.radio_utils import RadioUtils
from api.utils.radio_queue import RadioQueueManager
import logging
import traceback
from urllib.parse import urljoin

def setup_routes(app: bottle.Bottle, url_api_root: str, par_obj_radio_player: RadioPlayer, par_obj_radio_queue: RadioQueueManager):

    @app.route(url_api_root + '/player/', method=['GET','POST'])
    @app.route(url_api_root + '/player', method=['GET','POST'])
    def player_root():
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

        # Get parameter id
        var_id = None
        if("id" in posted_data):
            var_id = posted_data.get('id')
        else:
            var_param_id = bottle.request.params.get("id")
            if(var_param_id is not None):
                var_id = int(var_param_id)

        # If action is "toggle-play-pause"
        if var_action == "toggle-play-pause":
            try:
                par_obj_radio_player.toggle_play_pause()
                var_return_json = RadioUtils.generate_return_dict(True)
            except Exception as e:
                var_error_message = "Error when toggling play/pause."
                logging.error(f"{var_error_message} : {traceback.format_exc()}")
                bottle.abort(500,var_error_message)

        # If action is "next"
        elif var_action == "next":
            try:
                if par_obj_radio_player.next(): 
                    var_return_json = RadioUtils.generate_return_dict(True)
                else:
                    var_return_json = RadioUtils.generate_return_dict(True,None,"It is impossible to go to the next song.")
            except Exception as e:
                var_error_message = "Error when going to the next song."
                logging.error(f"{var_error_message} : {traceback.format_exc()}")
                bottle.abort(500,var_error_message)

        # If action is "previous"
        elif var_action == "previous":
            try:
                if par_obj_radio_player.previous():
                    var_return_json = RadioUtils.generate_return_dict(True)
                else:
                    var_return_json = RadioUtils.generate_return_dict(True,None,"It is impossible to go to the previous song.")
            except Exception as e:
                var_error_message = "Error when going to the previous song."
                logging.error(f"{var_error_message} : {traceback.format_exc()}")
                bottle.abort(500,var_error_message)

        # If action is "play"
        elif var_action == "play":
            try:
                par_obj_radio_player.play(var_id)
                var_return_json = RadioUtils.generate_return_dict(True)
            except RadioPlayerBadSongIdError as e:
                var_return_json = RadioUtils.generate_return_dict(True,None,"Song id is incorrect.")
            except Exception as e:
                var_error_message = "Error when starting song."
                logging.error(f"{var_error_message} : {traceback.format_exc()}")
                bottle.abort(500,var_error_message)

        # If action is "stop"
        elif var_action == "stop":
            try:
                par_obj_radio_player.stop()
                var_return_json = RadioUtils.generate_return_dict(True)
            except Exception as e:
                var_error_message = "Error when stopping song."
                logging.error(f"{var_error_message} : {traceback.format_exc()}")
                bottle.abort(500,var_error_message)

        # If there is no action or an invalid action, then show help
        else:
            var_root_dict = {
                "ressources" : [
                    {
                        "name" : "Player manipulation",
                        "uri" : url_api_root + "/player",
                        "url" : bottle.request.url.strip("/"),
                        "methods" : "GET, POST",
                        "description" : "Allow to manipulate player with action parameter. The main parameter is 'action' ",
                        "action=toggle-play-pause" : "If the music is playing, then it is stopped. If the music is paused or stopped, then it starts.",
                        "action=next" : "Set the current playing song on the next in the queue.",
                        "action=previous" : "Set the current playing song on the previous in the queue.",
                        "action=play" : "Start playing the current song. Go on the first song is not playing. If parameter 'id' is provided, start playing song with this id in queue.",
                        "action=stop" : "Stop playing the current song.",
                    },
                    {
                        "name" : "Status",
                        "uri" : url_api_root + "/player/status",
                        "url" : bottle.request.url.strip("/") + "/status",
                        "methods" : "GET",
                        "description" : "Return player's status with several attributes : state, playlistlength, current_song_number, elapsed, duration, current item, volume datas."
                        },
                    {
                        "name" : "Volume",
                        "uri" : url_api_root + "/player/volume",
                        "url" : bottle.request.url.strip("/") + "/volume",
                        "methods" : "GET, POST",
                        "description" : "Allow to manipulate sound volume. If no parameter is provided, return current volume range (0-100).",
                        "action=set-range&range=<xxx>" : "Change volume range to <xxx> value. This value must be between 0 and 100.",
                    }
                ]
            }
            var_return_json = RadioUtils.generate_return_dict(True,var_root_dict)

        
        return var_return_json

    @app.route(url_api_root + '/player/status', method=['GET'])
    def status():
        var_return_json = {}
        
        try:
            # Get status
            var_status = par_obj_radio_player.get_status()

            # Get current item
            var_current_song_json = {}
            if var_status.current_song_number >= 0 and var_status.current_song_id >= 0:
                var_obj_radio_queue_item = par_obj_radio_queue.get_item(var_status.current_song_id)
                if var_obj_radio_queue_item is not None:
                    var_current_song_json = {
                        "title" : var_obj_radio_queue_item.queued_item.title,
                        "name" : var_obj_radio_queue_item.queued_item.name,
                        "artist" : var_obj_radio_queue_item.queued_item.artist,
                        "album" : var_obj_radio_queue_item.queued_item.album,
                        "file" : var_obj_radio_queue_item.queued_item.file,
                        "mr_stream_name" : var_obj_radio_queue_item.queued_item.mr_stream_name,
                        "mr_playlist_index" : var_obj_radio_queue_item.queued_item.mr_playlist_index,
                        "mr_playlist_name" : var_obj_radio_queue_item.queued_item.mr_playlist_name
                    }

            # Make result
            var_status_dict = {
                "state" : var_status.state,
                "playlistlength" : var_status.playlistlength,
                "current_song_number" : var_status.current_song_number,
                "current_song_id" : var_status.current_song_id,
                "current_song_item" : var_current_song_json,
                "elapsed" : var_status.elapsed,
                "duration" : var_status.duration,
                "queue_version" : var_status.queue_version,
                "db_refreshing" : "true" if var_status.db_refreshing else "false",
                "volume" : var_status.volume
            }
            var_return_json = RadioUtils.generate_return_dict(True, var_status_dict)
        except Exception as e:
            var_error_message = "Error when getting status."
            logging.error(f"{var_error_message} : {traceback.format_exc()}")
            bottle.abort(500,var_error_message)

        return var_return_json

    @app.route(url_api_root + '/player/volume/', method=['GET','POST'])
    @app.route(url_api_root + '/player/volume', method=['GET','POST'])
    def volume():
        var_return_json = {}

        logging.error("Test")

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

        # Get range
        var_range = 0
        if("range" in posted_data):
            var_range = int(posted_data.get('range'))
        else:
            var_param_range = bottle.request.params.get("range")
            if(var_param_range is not None):
                var_range = int(var_param_range)

        # If action is "set-range"
        if var_action == "set-range":
            try:
                par_obj_radio_player.set_volume_range(var_range)
                var_return_json = RadioUtils.generate_return_dict(True)
            except Exception as e:
                var_error_message = "Error when setting volume range."
                logging.error(f"{var_error_message} : {traceback.format_exc()}")
                bottle.abort(500,var_error_message)

        # If there is no action or an invalid action, then getting volume
        else:
            # Get status
            var_status = par_obj_radio_player.get_status()

            # Make result
            var_status_dict = {
                "volume" : var_status.volume
            }
            var_return_json = RadioUtils.generate_return_dict(True, var_status_dict)

        return var_return_json
