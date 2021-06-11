import requests
import json
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
                             object_type: str,
                             url: str,
                             **kwargs: dict):
        # wrapper for API calls to handle pagination
        headers = {
                'Authorization': 'Bearer ' + self.private_token
                }
        
        response = requests.get(url     = url,
                                headers = headers,
                                **kwargs)
        
        if response.status_code == 200:
            # Load Response data into dict
            data = json.loads(response.content)
            
            # Handle Pagination
            pagination = data['pagination']
            
            if not pagination['has_more_items']:
                # If no additional requests are required
                return data[object_type]
            else:
                # If we need to handle pagination
                current_page = pagination['page_number']
                total_pages = pagination['page_count']
                # Create list to bind results
                output_list = []
                while pagination['has_more_items']:
                    # handle requesting and re-requesting
                    # for multiple pages
                    continued_url = url + '?continuation=' + pagination['continuation']
                    
                    # perform the request again using the continuation url
                    response = requests.get(url     = continued_url,
                                            headers = headers,
                                            **kwargs)
                    
                    data = json.loads(response.content)
                    
                    pagination = data['pagination']
                    output_list.append(data[object_type])
                
                return output_list
        else:
            # If response status code is not 200
            return None
        

        
    def list_my_organizations(self):
            # method to list organizations a user has access to
            url = self._base_url + '/users/me/organizations/'
            
            response = self._get_request_wrapper(object_type = 'organizations',
                                                 url = url)
            
            return response
        
    def get_venue(self,
                  venue_id: str
                  ) -> dict:
        # method to get venue by id
        url = self._base_url + f'/venues/{venue_id}/'
        
        response = self._get_request_wrapper(object_type = 'venues',
                                             url = url)
            
        return response

        

my_api = EventBriteApi()

response = my_api.list_my_organizations()