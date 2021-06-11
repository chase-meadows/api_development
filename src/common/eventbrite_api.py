import requests
from dotenv import dotenv_values


# Load .Env Variables as config
config = dotenv_values('.env')

# EventBrite Api class wrapper to handle 
# API requests
class EventBriteApi(object):
    def __init__(self):
        self.private_token = config.get('EVENTBRITE_PRIVATE_TOKEN')
        self._api_version = 3
        self._base_url = 'https://www.eventbriteapi.com/v3/'
        
        
    def _get_request_wrapper(self,
                             url: str,
                             data: dict):
        # wrapper for API calls to handle pagination
        headers = {
                'Authorization': 'Bearer ' + self.private_token
                }
        
        response = requests.get(url     = url,
                                headers = headers,
                                data    = data)
        
        if response.status_code == 200:
            # figure out how we want to handle response codes and failures
            return response
        else:
            return response
        
        def list_my_organizations(self):
            # method to list organizations a user has access to
            url = self._base_url + '/users/me/organizations/'
            
            response = self._get_request_wrapper(url = url,
                                                 data = data)
            
            return response
        

my_api = EventBriteApi()

response = my_api.list_my_organizations()