import bottle
import os
from api.radio_api_app import RadioApiApp


class RadioWebClientApp:
    def initialize(app: bottle.Bottle):
        """ Initialize route to web client site.

        Args:
            app (Bottle): _Bottle application object.

        Returns:
            HTTPResponse : Response that contains requested file
        """
        # Get absolute path of web client file
        var_absolute_script_path = os.path.dirname(os.path.abspath(__file__))
        
        # Define template directory
        bottle.TEMPLATE_PATH.insert(0, os.path.join(var_absolute_script_path, 'views'))
        
        @app.route(RadioWebClientApp.get_path())
        @app.route(RadioWebClientApp.get_path() + '/index.html')
        def web_client_wrong_root():
            return bottle.redirect(RadioWebClientApp.get_path() + '/')
        
        @app.route(RadioWebClientApp.get_path() + '/')
        def web_client_root():
            var_api_url = f"{bottle.request.urlparts.scheme}://{bottle.request.urlparts.netloc}{RadioApiApp.get_path()}"
            return bottle.template("index.html", api_url = var_api_url)

        @app.route(RadioWebClientApp.get_path() + '/<filepath:path>')
        def web_client_file(filepath):
            return bottle.static_file(filepath, root=var_absolute_script_path)

    def get_path():
         return "/webclient";