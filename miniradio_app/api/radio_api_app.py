import bottle
from api.utils.radio_connection import RadioConnection
from radio_config import RadioUiConfig
from api.utils.radio_item_display_manager import ItemDisplayManager
from api.utils.radio_utils import RadioUtils
from api.utils.radio_player import RadioPlayer
from api.utils.radio_queue import RadioQueueManager
from api.utils.radio_playlists import RadioPlaylists
from api.utils.radio_folders import RadioFolders
from api.utils.radio_settings import RadioSettings
from api.business_ressources import player, utils, playlists, queue, folders, settings

class RadioApiApp:
    def initialize(parBottleApp: bottle.Bottle, parConfig: RadioUiConfig):
        # Get radio player connection
        var_radio_connexion = RadioConnection(parConfig.getMpdAddress(), parConfig.getMpdPort())
        var_radio_connexion.check_connection()

        # Get items display manager
        var_obj_item_display_manager = ItemDisplayManager()

        # Get player manager
        var_obj_radio_player = RadioPlayer(var_radio_connexion)

        # Get Queue manager
        var_obj_radio_queue = RadioQueueManager(var_radio_connexion, var_obj_item_display_manager)

        # Get playlists manager
        var_obj_radio_playlists = RadioPlaylists(var_radio_connexion, var_obj_item_display_manager, parConfig)

        # Get folders manager
        var_obj_radio_folders = RadioFolders(var_radio_connexion, var_obj_item_display_manager)

        # Get config manager
        var_obj_radio_settings = RadioSettings(var_radio_connexion)

        # Set routes
        player.setup_routes(parBottleApp, RadioApiApp.get_path(), var_obj_radio_player, var_obj_radio_queue)
        playlists.setup_routes(parBottleApp, RadioApiApp.get_path(), var_obj_radio_playlists, var_obj_radio_queue, var_obj_radio_player)
        folders.setup_routes(parBottleApp, RadioApiApp.get_path(), var_obj_radio_folders, var_obj_radio_queue, var_obj_radio_player)
        queue.setup_routes(parBottleApp, RadioApiApp.get_path(), var_obj_radio_queue)
        settings.setup_routes(parBottleApp, RadioApiApp.get_path(), var_obj_radio_settings, var_obj_radio_playlists)
        utils.setup_routes(parBottleApp, RadioApiApp.get_path(), var_radio_connexion, parConfig.getRunMode())

    def get_path():
         return "/api";