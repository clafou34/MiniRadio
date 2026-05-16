import bottle
import os
from radio_config import RadioUiConfig
from api.radio_api_app import RadioApiApp
from webclient.radio_web_client_app import RadioWebClientApp


class RadioRootApp:
    def initialize(app: bottle.Bottle, parConfig: RadioUiConfig):
        @app.route('/')
        @app.route('/index.html')
        def miniradio_root():
            var_index_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "views", "index.html")
        
            with open(var_index_path, 'r', encoding='utf-8') as index_file:
                var_content = index_file.read()                         

            return bottle.template(var_content, 
                url_web_client = RadioWebClientApp.get_path() if parConfig.getUseWebClient() else "",
                url_api = RadioApiApp.get_path()
                )

                
