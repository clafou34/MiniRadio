from api.utils.radio_item import RadioItem
import os

class ItemDisplayManager:
    def __init__(self):
        # List of stream that are webradio
        self.__var_stream_item_list: list[RadioItem] = []

    def set_stream_item_list(self, par_list: list[RadioItem]):
        self.__var_stream_item_list = par_list

    def parse_song_item(self, par_song, par_complete_with_cache: bool = True) -> RadioItem:
        """
        Create an RadioItem with complement data for playlist an item.
        
        :param par_song: Dictionnary that contain data from an item supplied by API.

        :param par_complete_with_cache: If True, then stream data are search in cache and merge in result object.
        :type par_complete_with_cache: bool

        :return: Object that contains all attributes necessary for diplaying playlist item.
        :rtype: RadioItem
        """
        var_obj_item = RadioItem()
        var_obj_item.file = par_song['file']
        if var_obj_item.file.startswith("http://") or var_obj_item.file.startswith("https://"):
            var_obj_item.title = par_song['title'] if 'title' in par_song else ""
        else:
            var_obj_item.title = par_song['title'] if 'title' in par_song else os.path.basename(par_song['file']).split('.')[0]
        var_obj_item.name = par_song['name'] if 'name' in par_song else ""
        var_obj_item.album = par_song['album'] if 'album' in par_song else ""
        var_obj_item.artist = par_song['artist'] if 'artist' in par_song else ""
        var_obj_item.date = par_song['date'] if 'date' in par_song else ""
        var_obj_item.genre = par_song['genre'] if 'genre' in par_song else ""

        # Set extended stream data
        if (par_complete_with_cache) and (var_obj_item.file in self.__var_stream_item_list) and (var_obj_item.file.startswith("http://") or var_obj_item.file.startswith("https://")):
            var_obj_item.mr_stream_name = self.__var_stream_item_list[var_obj_item.file].mr_stream_name
            var_obj_item.mr_playlist_index = self.__var_stream_item_list[var_obj_item.file].mr_playlist_index
            var_obj_item.mr_playlist_name = self.__var_stream_item_list[var_obj_item.file].mr_playlist_name
            var_obj_item.name = var_obj_item.mr_stream_name


        return var_obj_item
    