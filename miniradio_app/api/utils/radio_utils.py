import re

class RadioUtils:
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

