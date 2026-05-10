import configparser
import logging
import os
from pathlib import Path
import json

class RadioUiConfigError(Exception):
    pass

class RadioConfigWebradiosError(Exception):
    pass

class RadioUiConfig:
    __run_mode: str # "DEBUG" or "NORMAL"
    __address: str
    __port: int
    __use_web_client: str # "True" or "False"
    __file_config_path: str
    __file_pl_config_path: str

    
    def __init__(self, par_dir_config_path: str = ""):
        """
        Create a configuration object from the data in the file whose path is provided in the parameter 'par_file_config_path'.
        If the configuration file not exists, it will be created.

        Args:
            par_dir_config_path (str, optional): Configuration dir path. Defaults to "__file__/configuration".

        """
        config_structure = configparser.ConfigParser()
        fileToSave = False
        
        ##############################
        ## Initialize path
        ##############################
        var_dir_config_path = par_dir_config_path
        if var_dir_config_path=="":
            self.__file_config_path = "radioui.conf"
            self.__file_pl_config_path = "webradios_pl_config.json"
        else:
            self.__file_config_path = os.path.join(par_dir_config_path,"radioui.conf")
            self.__file_pl_config_path = os.path.join(par_dir_config_path,"webradios_pl_config.json")

        ##############################
        ## Open config file
        ##############################
        try:
            file_stream = open(self.__file_config_path)
            config_structure.read_file(file_stream)
            file_stream.close()
        except (FileNotFoundError, configparser.MissingSectionHeaderError) as fileError:
            logging.warning("Error when reading file \"" + self.__file_config_path + "\" : " + str(fileError))
            logging.warning("Creating new config file.")
            # Init file with default values
            config_structure.add_section('mpd.connexion')

            # Creating config file
            var_dir_config = os.path.dirname(self.__file_config_path)
            if len(var_dir_config) > 0:
                if not os.path.isdir(var_dir_config): # Si le répertoire du fichier n'existe pas
                    logging.warning("Creating new directory \"" + var_dir_config + "\"")
                    os.makedirs(name=var_dir_config, exist_ok=True)
            file_stream = open(self.__file_config_path, 'w')
            config_structure.write(file_stream)
            file_stream.close()
            
                
        ##############################
        # Read config file
        ##############################
        
        ## Read Global section
        if not config_structure.has_section('global'):
            config_structure.add_section('global')
            fileToSave = True
                    
        try:
            self.__run_mode = config_structure.get('global', 'run-mode')
        except configparser.NoOptionError:
            logging.warning("Creating run-mode option with \"NORMAL\" value.")
            self.__run_mode = "NORMAL"
            config_structure.set('global', 'run-mode', "NORMAL")
            fileToSave = True
        
        if(self.__run_mode not in ("DEBUG","NORMAL")):
            raise RadioUiConfigError("\"run-mode\" option should be \"DEBUG\" or \"NORMAL\".")

        ## Read mpd.connexion section
        if not config_structure.has_section('mpd.connexion'):
            config_structure.add_section('mpd.connexion')
            fileToSave = True

        try:
            self.__address = config_structure.get('mpd.connexion', 'address')
        except configparser.NoOptionError:
            logging.warning("Creating address option.")
            self.__address = "localhost"
            config_structure.set('mpd.connexion', 'address', "localhost")
            fileToSave = True
            
        try:
            self.__port =  int(config_structure.get('mpd.connexion', 'port'))
        except configparser.NoOptionError:
            logging.warning("Creating port option.")
            self.__port = 6600
            config_structure.set('mpd.connexion', 'port', "6600")
            fileToSave = True
        except ValueError:
            logging.warning("In config file, port in not an integer. Setting default value 6600.")
            self.__port = 6600
            config_structure.set('mpd.connexion', 'port', "6600")
            fileToSave = True

        ## Read web.client section
        if not config_structure.has_section('web.client'):
            config_structure.add_section('web.client')
            fileToSave = True

        try:
            self.__use_web_client = config_structure.get('web.client', 'use-web-client')
        except configparser.NoOptionError:
            logging.warning("Creating use-web-client option with \"False\" value.")
            self.__use_web_client = "False"
            config_structure.set('web.client', 'use-web-client', "False")
            fileToSave = True

        ####################################
        # Save file if it is modified
        ####################################
        if fileToSave:
            file_stream = open(self.__file_config_path, 'w')
            config_structure.write(file_stream)
            file_stream.close()
    
    def getRunMode(self) -> str:
        return self.__run_mode
    
    def getAddress(self) -> str:
        return self.__address
    
    def getPort(self) -> str:
        return self.__port
    
    def getUseWebClient(self) -> bool :
        return self.__use_web_client == "True"
    
    def readWebradiosPlConfig(self):
        json_webradios_pl = []

        try:
            with open(self.__file_pl_config_path, 'r', encoding='utf-8') as file_pl_json:
                json_raw_data = json.load(file_pl_json)

            for json_item in json_raw_data:
                if "name" in json_item and "filename" in json_item:
                    json_webradios_pl.append({"name" : json_item["name"], "filename" : json_item["filename"]})

        except FileNotFoundError as e:
            logging.warning(f"Webradios playlists configuration file '{self.__file_pl_config_path}' not found. List is initialized as empty.")
        except Exception as e:
            raise RadioConfigWebradiosError("Error when loading all webradios playlists configuration.") from e

        return json_webradios_pl
    