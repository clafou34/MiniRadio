from mpd import MPDClient, CommandError
import logging
from api.utils.radio_utils import RadioItem
from api.utils.radio_connection import RadioConnection

class RadioPlayerError(Exception):
    pass

class RadioPlayerBadSongIdError(Exception):
    pass

class RadioPlayerStatus:
    def __init__(self):
        self.state: str = "" # 3 values possible : play, pause, stop
        self.playlistlength: int = 0 # the length of the playlist
        self.current_song_number: int = None
        self.current_song_id: int = None
        self.elapsed: float
        self.duration: float
        self.queue_version: int = 0
        self.db_refreshing: bool = False

class RadioPlayer:  
    def __init__(self, par_radio_connection: RadioConnection):
        self.__var_mpd_client: MPDClient = par_radio_connection.get_mpd_client()
    
    def toggle_play_pause(self):
        try:
            var_dict_status = self.__var_mpd_client.status()
            if var_dict_status['state'] == "stop":
                self.__var_mpd_client.play();
            else:
                self.__var_mpd_client.pause()
        except Exception as e:
            raise RadioPlayerError("Error when toggling player state.") from e

    def get_status(self) -> RadioPlayerStatus :
        var_player_status = RadioPlayerStatus()
        
        try:
            var_dict_status = self.__var_mpd_client.status()
            var_player_status.state = var_dict_status['state']
            var_player_status.playlistlength = int(var_dict_status['playlistlength'])
            if 'elapsed' in var_dict_status:
                var_player_status.elapsed = float(var_dict_status['elapsed'])
            else:
                var_player_status.elapsed = -1
            if 'duration' in var_dict_status:
                var_player_status.duration = float(var_dict_status['duration'])
            else:
                var_player_status.duration = -1
            if 'song' in var_dict_status:
                var_player_status.current_song_number = int(var_dict_status['song'])
            else:
                var_player_status.current_song_number = -1
            if 'songid' in var_dict_status:
                var_player_status.current_song_id = int(var_dict_status['songid'])
            else:
                var_player_status.current_song_id = -1
            if 'playlist' in var_dict_status:
                var_player_status.queue_version = int(var_dict_status['playlist'])
            else:
                var_player_status.queue_version = 0
            if 'updating_db' in var_dict_status:
                var_player_status.db_refreshing = True
            else:
                var_player_status.db_refreshing = False
        except Exception as e:
            raise RadioPlayerError("Error when getting player status.") from e
            
        return var_player_status
    
    def next(self) -> bool:
        """Set next song to be played. Return True if going to next song is done, and
        return False if is not possible.

        Raises:
            RadioPlayerError: Exception raised if an unexpected error occurs. 

        Returns:
            bool : True if going to next song is done, and return False if is not possible.
        """
        var_ret = True
        try:
            var_status = self.get_status()
            if var_status.current_song_number < (var_status.playlistlength -1) and var_status.current_song_number >= 0 and var_status.state != "stop":
                self.__var_mpd_client.next()
            else:
                var_ret = False
        except Exception as e:
            raise RadioPlayerError("Error when passing to the next song.") from e

        return var_ret
    
    def previous(self) -> bool:
        """Set previous song to be played. Return True if going to previous song is done, and
        return False if is not possible.

        Raises:
            RadioPlayerError: Exception raised if an unexpected error occurs. 

        Returns:
            bool : True if going to previous song is done, and return False if is not possible.
        """
        var_ret = True
        try:
            var_status = self.get_status()
            if var_status.state != "stop":
                self.__var_mpd_client.previous()
            else:
                var_ret = False
        except Exception as e:
            raise RadioPlayerError("Error when passing to the previous song.") from e
        
        return var_ret

    def play(self, par_song_id:int = None):
        try:
            if par_song_id is None:
                self.__var_mpd_client.play()
            else:
                self.__var_mpd_client.playid(par_song_id)
        except CommandError as e:
            if(e.msg == "No such song"):
                raise RadioPlayerBadSongIdError("Bad song id to play.")
            else:
                raise RadioPlayerError("Error when starting song.") from e
        except Exception as e:
            raise RadioPlayerError("Error when starting song.") from e

    def stop(self):
        try:
            self.__var_mpd_client.stop()
        except Exception as e:
            raise RadioPlayerError("Error when stopping song.") from e
