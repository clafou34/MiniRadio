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

class RadioFolderContent:
    def __init__(self):
            self.folders:list[RadioFolder] = []
            self.items:list[RadioItem] = []
     
class RadioFolder:
    def __init__(self, par_folder_name:str = "", par_folder_path:str = ""):
            self.name:str = par_folder_name
            self.path:str = par_folder_path

