from mpd import MPDClient, CommandError
from api.utils.radio_utils import RadioItem
from api.utils.radio_connection import RadioConnection
from api.utils.radio_item_display_manager import ItemDisplayManager
from urllib.parse import urlparse

class RadioQueueItem:
    def __init__(self):
        self.id: int
        self.pos: int
        self.queued_item: RadioItem

class RadioQueueError(Exception):
    pass

class RadioQueueNotFoundError(Exception):
    pass

class RadioQueueManager:

    def __init__(self, par_radio_connection: RadioConnection, par_item_display_manager: ItemDisplayManager):
        # Get MPD connexion
        self.__var_mpd_client: MPDClient = par_radio_connection.get_mpd_client()

        # Get stream item display cache
        self.__var_item_display_manager: ItemDisplayManager = par_item_display_manager
        
    def get_items(self):
        var_obj_queue_item_list = []
        
        try:
            var_songs_list = self.__var_mpd_client.playlistinfo()
            
            for var_song in var_songs_list:
                var_obj_queue_item = RadioQueueItem()
                var_obj_queue_item.queued_item = self.__var_item_display_manager.parse_song_item(var_song)
                var_obj_queue_item.id = var_song['id']
                var_obj_queue_item.pos = var_song['pos']

                var_obj_queue_item_list.append(var_obj_queue_item)
            
            return var_obj_queue_item_list
        except Exception as e:
            raise RadioQueueError(f"Error when getting items of queue.") from e
    
    def get_item(self, par_item_id:int) -> RadioQueueItem:
        """
        Return a RadioQueueItem class object for song in queue with "par_item_id" as identifier.
        
        :param par_item_id: Id of item in queue
        :type par_item_id: int
        :return: Object for song in queue with "par_item_id" as identifier.
        :rtype: RadioQueueItem
        """
        try:
            
            var_obj_queue_item = None
            var_songs_list = self.__var_mpd_client.playlistid(par_item_id)
            
            if len(var_songs_list)>0:
                var_song = var_songs_list[0]

                var_obj_queue_item = RadioQueueItem()
                var_obj_queue_item.queued_item = self.__var_item_display_manager.parse_song_item(var_song)
                var_obj_queue_item.id = var_song['id']
                var_obj_queue_item.pos = var_song['pos']
            
            return var_obj_queue_item

        except CommandError as e:
            if(e.msg == "No such song"):
                raise RadioQueueNotFoundError from e
            else:
                raise RadioQueueError(f"Error when delete item from queue.") from e
        except Exception as e:
            raise RadioQueueError(f"Error when getting item from queue.") from e        
    
    def delete_item(self, par_item_id:int):
        """Remove an item from queue list.

        Args:
            par_item_id (int): Id of item to remove

        Raises:
            RadioQueueNotFoundError: There is no item with "par_item_id"
            RadioQueueError: Raised when an unknown error occur
        """
        try:
            self.__var_mpd_client.deleteid(par_item_id)
        except CommandError as e:
            if(e.msg == "No such song"):
                raise RadioQueueNotFoundError from e
            else:
                raise RadioQueueError(f"Error when delete item from queue.") from e
        except Exception as e:
            raise RadioQueueError(f"Error when delete item from queue.") from e
    
    def add_radio_item(self, par_radio_item: RadioItem):
        """
        Add an RadioItem in MPD queue and put it on cache to preserve display information.
        
        :param par_radio_item: RadioItem class objet that contains url (attribute file) to add in mpd queue. Complementaries attributes
        are saved in cache for displaying.
        :type par_radio_item: RadioItem
        """
        var_item_id = None
        try:
            var_item_id = self.__var_mpd_client.addid(par_radio_item.file)
        except Exception as e:
            raise RadioQueueError(f"Error when adding items in queue.") from e       

    def clear(self):
        """
        Remove all item from queue.
        """
        try:
            self.__var_mpd_client.clear()
        except Exception as e:
            raise RadioQueueError(f"Error when clearing queue.") from e             