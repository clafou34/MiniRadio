from mpd import MPDClient, CommandError, FailureResponseCode
from api.utils.radio_connection import RadioConnection
from api.utils.radio_item import RadioItem, RadioFolder, RadioFolderContent

from api.utils.radio_item_display_manager import ItemDisplayManager
import os

class RadioFoldersError(Exception):
    pass

class RadioFoldersNoExistError(Exception):
    pass

class RadioFolders:
    def __init__(self, par_radio_connection: RadioConnection, par_item_display_manager: ItemDisplayManager):
        self.__var_mpd_client: MPDClient = par_radio_connection.get_mpd_client()

        # Get stream item display cache
        self.__var_item_display_manager: ItemDisplayManager = par_item_display_manager

    def get_content(self, par_folder_uri:str = "") :
        var_folder_content_to_return:RadioFolderContent = RadioFolderContent()

        try:
            var_folder_list = self.__var_mpd_client.lsinfo(par_folder_uri)
            for var_content in var_folder_list:
                if "directory" in var_content:
                    if(var_content["directory"] != par_folder_uri):
                        var_folder_content_to_return.folders.append(
                            RadioFolder(
                                os.path.basename(os.path.normpath(var_content["directory"])),
                                var_content["directory"]
                                ))
                elif "file" in var_content:
                    var_folder_content_to_return.items.append(self.__var_item_display_manager.parse_song_item(var_content))
        except CommandError as e:
            if(e.errno == FailureResponseCode.NO_EXIST):
                raise RadioFoldersNoExistError("Error getting folder content.") from e
            else:
                raise RadioFoldersError("Error getting folder content.") from e
        except Exception as e:
            raise RadioFoldersError("Error getting folder content.") from e


        return var_folder_content_to_return
