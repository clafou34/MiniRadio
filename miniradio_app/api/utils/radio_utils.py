import json
import re

class RadioFolderContent:
    def __init__(self):
            self.folders:list[RadioFolder] = []
            self.items:list[RadioItem] = []
     

class RadioFolder:
    def __init__(self, par_folder_name:str = "", par_folder_path:str = ""):
            self.name:str = par_folder_name
            self.path:str = par_folder_path

class RadioItem:
    def __init__(self, par_title:str = "", par_name:str = "", par_file:str = "", par_artist:str = "", par_album:str = "", par_date:str = "", par_genre:str = "", par_mr_stream_name:str = "", par_mr_playlist_name:str = "", par_mr_playlist_index:str = ""):
        self.title:str = par_title
        self.name:str = par_name
        self.file:str = par_file
        self.artist:str = par_artist
        self.album:str = par_album
        self.date:str = par_date
        self.genre:str = par_genre
        self.mr_stream_name:str = par_mr_stream_name
        self.mr_playlist_name:str = par_mr_playlist_name
        self.mr_playlist_index:str = par_mr_playlist_index

def generate_return_dict(par_success:bool = True, par_payload:dict = None, par_error_message:str = "") -> dict:
    var_dict = {
        "success" : "OK" if par_success else "KO",
    }
    
    if par_error_message != "":
        var_dict["error_message"] = par_error_message
    
    if par_payload is not None:
        var_dict["payload"] = par_payload
    
    return var_dict

def remove_url_last_part(par_url:str) -> str:
    '''
    Removes the last segment of a URL (everything after the last slash). If the result URL ends with a slash, it is also removed.
    
    :param par_url: Url on the last part must be removed.
    :type par_url: str
    :return: Url without her last part.
    :rtype: str
    '''
    return re.sub(r'/[^/]+/?$', '', par_url)
