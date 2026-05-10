from mpd import MPDClient, CommandError
from api.utils.radio_connection import RadioConnection

class RadioConfigError(Exception):
    pass

class RadioSettings:  
    def __init__(self, par_radio_connection: RadioConnection):
        self.__var_mpd_client: MPDClient = par_radio_connection.get_mpd_client()
        
    
    def refresh_db(self):
        try:
            self.__var_mpd_client.update()
        except Exception as e:
            raise RadioConfigError("Error when launching database update.") from e
