import logging
from mpd import MPDClient, ConnectionError

class RadioConnectionError(Exception):
    pass

class RadioConnection:
    
    def __init__(self, par_hostname: str = "hostname", par_port: int = 6600):
        self.__var_hostname: str = par_hostname
        self.__var_port: int = par_port
        self.__var_mpd_client: MPDClient = MPDClient()
        self.__var_mpd_client.timeout = 10
    
    def __connect(self):
        # Create MPD connexion
        logging.info(f"Connecting to MPD on {self.__var_hostname}:{self.__var_port}.")
        try:
            self.__var_mpd_client.connect(self.__var_hostname, self.__var_port)
        except:
            var_str_error_message = f"Error at connexion to MPD on {self.__var_hostname}:{self.__var_port}. Try to check your configuration, your network connexion or that mpd working."
            raise RadioConnectionError(var_str_error_message)   
    
    def check_connection(self):
        """Check if the connexion to MPD server is OK. If it is not done, try to connect.
        """
        try:
            self.__var_mpd_client.ping()
        except ConnectionError:
            logging.info(f"Not connected to MPD server.")
            self.__connect()
            
    def get_hostname(self) -> str:
        return self.__var_hostname
    
    def get_port(self) -> int:
        return self.__var_port
    
    def get_mpd_client(self) -> MPDClient:
        return self.__var_mpd_client
