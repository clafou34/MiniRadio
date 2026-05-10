#from bottle import Bottle, static_file, redirect, TEMPLATE_PATH
import bottle
import logging
import os

def setup_routes(app: bottle.Bottle, par_path_root, url_web_client_root: str, url_api_root: str):
    """ Define route to web client site.

    Args:
        par_path_root (str) : String than contain the root path of scripts
        app (Bottle): _Bottle application object.
        url_web_client_root (str): Web Client site root in URL (ex : "/web-client")

    Returns:
        HTTPResponse : Response that contains requested file
    """
    # Get absolute path of web client file
    var_absolute_script_path = os.path.join(par_path_root, "webclient")
    
    # Define template directory
    bottle.TEMPLATE_PATH.insert(0, os.path.join(var_absolute_script_path, 'views'))
    
    @app.route(url_web_client_root)
    @app.route(url_web_client_root + '/index.html')
    def web_client_wrong_root():
        return bottle.redirect(url_web_client_root + '/')
    
    @app.route(url_web_client_root + '/')
    def web_client_root():
        var_api_url = f"{bottle.request.urlparts.scheme}://{bottle.request.urlparts.netloc}{url_api_root}"
        return bottle.template("index.html", api_url = var_api_url)

    @app.route(url_web_client_root + '/<filepath:path>')
    def web_client_file(filepath):
        return bottle.static_file(filepath, root=var_absolute_script_path)