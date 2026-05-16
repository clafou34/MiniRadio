from mpd import MPDClient
from radio_config import RadioUiConfig
from api.utils.radio_connection import RadioConnection
from api.utils.radio_item import RadioItem
from api.utils.radio_item_display_manager import ItemDisplayManager
from urllib.parse import urlparse
import time
import logging

class RadioPlaylistsError(Exception):
    pass

class RadioPlaylistsPlaylist:
    def __init__(self):
        self.index: int
        self.name: str
        self.filename: str
        self.type: str # "webradio" or "other"

class RadioPlaylists:
    
    __var_cache_retention:int = 600  # Cache retention duration is second

    def __init__(self, par_radio_connection: RadioConnection, par_item_display_manager: ItemDisplayManager, par_obj_config: RadioUiConfig):
        self.__var_mpd_client: MPDClient = par_radio_connection.get_mpd_client()

        # List of playlist objects used as cache performance.
        self.__current_playlists: list[RadioPlaylistsPlaylist] = None

        # Configuration objet for getting webradios playlists files
        self.__obj_config: RadioUiConfig = par_obj_config

        # Last date of cache update.
        self.__var_cache_time = time.time()

        # Initialise items stream display cache
        self.__var_item_display_manager = par_item_display_manager

        # Fill caches
        self.load_playlist()
    
    def load_playlist(self):
        """Load playlist from MPD in cache.
        
        Raises:
            RadioPlaylistsError: Raise if an error occurs.
        """

        try:
            self.__current_playlists = []
            
            var_list_playlist = self.__var_mpd_client.listplaylists()

            var_webradios_playlists_files = self.__obj_config.readWebradiosPlConfig()
            
            # Get all playlists
            var_index = 0
            for var_playlist in var_list_playlist:
                var_obj_playlist = RadioPlaylistsPlaylist()
                
                var_webradio_playlist = next((d for d in var_webradios_playlists_files if d["filename"] == var_playlist['playlist']), None)
                
                var_obj_playlist.index = var_index
                var_obj_playlist.name = var_playlist['playlist']
                if var_webradio_playlist is not None:
                    var_obj_playlist.type = "webradio"
                    if var_webradio_playlist["name"] != "":
                        var_obj_playlist.name = var_webradio_playlist["name"]
                else:
                    var_obj_playlist.type = "other"
                var_obj_playlist.filename = var_playlist['playlist']
                self.__current_playlists.append(var_obj_playlist)
                var_index += 1
            
            # Sort by playlist name
            self.__current_playlists.sort(key=lambda obj: obj.name)

            # Get content of all playlists
            self.__var_item_display_manager.set_stream_item_list(self.__filter_radio_stream_items(self.__current_playlists))

            # Set date of cache
            self.__var_cache_time = time.time()
            
        except Exception as e:
            logging.error("Error when loading all playlists.")
            raise RadioPlaylistsError("Error when loading all playlists.") from e
    
    def __clear_cache(self):
        self.__current_playlists = None

    def __get_cached_playlist(self):
        if (self.__current_playlists is None) or ((time.time() - self.__var_cache_time) > self.__var_cache_retention):
            self.load_playlist()

        return self.__current_playlists

    def __filter_radio_stream_items(self, par_list_all_playlist: list[RadioItem]):
        """
        Return a list of RadioItem of type 'webradio' retrieved from the list provided as a parameter.
        List is indexed by url of stream.

        Args:
            par_list_all_playlist (list[RadioItem], mandatory): List of RadioItem to be filtered.
        
        :return: List of RadioItem class objects which are stream.
        :rtype: list[RadioItem]
        """
        var_stream_item_list = {}

        try:
            for var_playlist in par_list_all_playlist:
                if var_playlist.type=="webradio":
                    var_songs_list = self.__var_mpd_client.listplaylistinfo(var_playlist.filename)
                    for var_song in var_songs_list:
                        if(var_song['file'].startswith("http://") or var_song['file'].startswith("https://")):
                            # Convert song in item
                            var_item = self.__var_item_display_manager.parse_song_item(var_song, False)

                            # Set specific attributes
                            if(var_item.name != ""):
                                var_item.mr_stream_name = var_item.name
                            else:
                                var_url_part = urlparse(var_item.file)
                                var_item.mr_stream_name = var_url_part.scheme + "://" + var_url_part.netloc.strip('/') + "/" + var_url_part.path.strip('/')
                            var_item.mr_playlist_index = var_playlist.index
                            var_item.mr_playlist_name = var_playlist.name
                            var_item.name = var_item.mr_stream_name

                            # Add item in list
                            var_stream_item_list[var_song['file']]=var_item

        except Exception as e:
            raise RadioPlaylistsError(f"Error when searching all items which are stream.") from e    

        return var_stream_item_list        

    def get_playlists(self, par_playlist_type: str = "all"):
        """Return a list of RadioPlaylistsPlaylist objects sorted alphabeticaly by name. This list
        contains all playlists that are in standard playlist directory.

        Args:
            par_playlist_type (str, optional): Playlists type to be selected. 3 values are possible "webradio", "other" or "all". Defaults to "all".

        Raises:
            RadioPlaylistsError: Raise if an error occurs.

        Returns:
            RadioPlaylistsPlaylist[]: List of RadioPlaylistsPlaylist
        """
        try:
            var_list_playlist = None
            var_playlist_type = None

            if(par_playlist_type in ["other","webradio"]):
                var_playlist_type = par_playlist_type
            else:
                var_playlist_type = "all"
            
            # Filter playlists with "type" parameter
            var_all_playlist = self.__get_cached_playlist()
            if var_playlist_type == "all":
                var_list_playlist = var_all_playlist
            else:
                var_list_playlist = (p for p in var_all_playlist if p.type == var_playlist_type)

            return var_list_playlist
        except Exception as e:
            logging.error("Error when loading all playlists.")
            raise RadioPlaylistsError("Error when getting all playlists.") from e

    def get_playlist(self, par_playlist_index: int):
        """Return the playlist whose index is passed as a parameter. If the playlist
        is not found, None is returned.

        Args:
            par_playlist_index (int): Index of the playlist searched.
        Raises:
            RadioPlaylistsError: Raise if an error occurs.

        Returns:
            RadioPlaylistsPlaylist: The playlist whose index is passed as a parameter. If the playlist
        is not found, None is returned.
        """
        var_obj_playlist = None
        var_all_playlist = self.__get_cached_playlist()
        
        try:
            var_playlist_found  = [var_playlist for var_playlist in var_all_playlist if var_playlist.index == par_playlist_index]
            if var_playlist_found:
                var_obj_playlist = var_playlist_found[0]
            
            return var_obj_playlist
        except Exception as e:
            raise RadioPlaylistsError(f"Error when getting playlist '{str(par_playlist_index)}'.") from e        

    def get_items(self, par_playlist_index: int):
        """Return a list of elements that are in the playlist whose index is passed as a parameter. If the playlist
        is not found, None is returned.

        Args:
            par_playlist_index (int): Index of the playlist from which item are being searched.
        Raises:
            RadioPlaylistsError: Raise if an error occurs.

        Returns:
            RadioItem[]: List of elements that are in the playlist whose index is passed as a parameter. If the playlist
        is not found, None is returned.
        """
        var_obj_item_list = []
        var_all_playlist = self.__get_cached_playlist()
        
        try:
            var_playlist_found  = [var_playlist for var_playlist in var_all_playlist if var_playlist.index == par_playlist_index]
            if var_playlist_found:
                var_songs_list = self.__var_mpd_client.listplaylistinfo(var_playlist_found[0].filename)
                
                for var_song in var_songs_list:
                    var_obj_item_list.append(self.__var_item_display_manager.parse_song_item(var_song))
            else:
                var_obj_item_list = None
            
            return var_obj_item_list
        except Exception as e:
            raise RadioPlaylistsError(f"Error when getting items of playlists '{str(par_playlist_index)}'.") from e            

    def get_item(self, par_playlist_index: int, par_item_index: int) -> RadioItem:
        """
        Get an item of one playlist.
        
        :param par_playlist_index: Playlist index that contains the item.
        :type par_playlist_index: int
        :param par_item_index: Item index in the playlist.
        :type par_item_index: int
        """
        var_all_playlist = self.__get_cached_playlist()
        var_item_found: RadioItem = None

        try:
            var_playlist_found  = [var_playlist for var_playlist in var_all_playlist if var_playlist.index == par_playlist_index]
            if var_playlist_found:
                var_songs_list = self.__var_mpd_client.listplaylistinfo(var_playlist_found[0].filename)
                if par_item_index < len(var_songs_list):
                    var_item_found = self.__var_item_display_manager.parse_song_item(var_songs_list[par_item_index])

        except Exception as e:
            raise RadioPlaylistsError(f"Error when getting items of playlists '{str(par_playlist_index)}'.") from e

        return var_item_found

        