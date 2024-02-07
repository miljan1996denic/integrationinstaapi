import json
import requests 

def getCreds():
    creds = dict()
    creds['access_token'] = 'EAAFYFGXaYlkBO7jlSMYQXWb6cXvAn8bF3C05LF5fCqioIdvJdogZCggXOTYgQCZBv3KMW9iY8WKLePgF1LYJBKqP0bOi5v0DdddXVGtRJrU1RZBpumJm9lZAOZAixL71XKiObvoxU975UA6bB2gsT3WUemBayVZBUJCgJg8IATSZBK8kZBZB4iGyRZBr43moMGNyur'
    creds['client_id'] = '378319608111705'
    creds['client_secret'] = '099e6f58e873919ac4c97d320bc621ee'
    creds['graph_domain'] = 'https://graph.facebook.com/'
    creds['graph_version'] = 'v18.0'
    creds['endpoint_base'] = creds['graph_domain'] + creds['graph_version'] + '/'
    creds['debug'] = 'no'
    # creds['page_id'] = '...' # this data should get from results of code in file get_insta_acc.py
    # creds['insta_acc_id'] = '...' # this data should get from results of code in file get_insta_acc.py
    creds['ig_username'] = "123petrapetrovic123"
    return creds

def makeApiCall(url, endpointParams, debug = 'no'):
    data = requests.get(url, endpointParams)

    response = dict()
    response['url'] = url
    response['endpoint_params'] = endpointParams
    response['endpoint_params_pretty'] = json.dumps(endpointParams, indent = 4)
    response['json_data'] = json.loads(data.content)
    response['json_data_pretty'] = json.dumps(response['json_data'], indent = 4)

    if( 'yes' == debug ):
        displayApiCallData(response)

    return response

def displayApiCallData(response):
    print("\nURL:")
    print(response['url'])
    print("\nEndpoint params:")
    print(response['endpoint_params_pretty'])
    print("\nResponse:")
    print(response['json_data_pretty'])


def getLongLivedAccessToken(params):
    
    # API Endpoint: https://graph.facebook.com/{graph-api-version}/oauth/access_token?grant_type=fb_exchange_token&client_id={app-id}&client_secret={app-secret}&fb_exchange_token={your-access-token}

    endpointParams = dict()
    endpointParams['grant_type'] = 'fb_exchange_token'
    endpointParams['client_id'] = params['client_id']
    endpointParams['client_secret'] = params['client_secret']
    endpointParams['fb_exchange_token'] = params['access_token']

    url = params['endpoint_base'] + 'oauth/access_token'
    return makeApiCall(url, endpointParams, params['debug'])

def debugAccessToken( params ):
    # Get info on an access token
    # API Endpoint: https://graph.facebook.com/debug_token?input_token={input-token}&access_token={valid-access-token}
    # returns: object: data from endpoint

    endpointParams = dict()
    endpointParams['input_token'] = params['access_token']
    endpointParams['access_token'] = params['access_token']

    url = params['graph_domain'] + '/debug_token'

    return makeApiCall(url, endpointParams, params['debug'])

def getAccountInfo(params):
    
    #API Endpoint: https://graph.facebook.com/{graph-api-version}/{ig-user-id}?fields=business_discovery.username({ig-username})({username}){username,website,ig_id,id,profile_picture_url,biography,follows_count,followers_count,media_count}&access_token={access-token}
    endpointParams = dict()
    endpointParams['fields'] = 'business_discovery.username(' + params['ig_username'] +'){username,website,ig_id,id,profile_picture_url,biography,follows_count,followers_count,media_count}'
    # del endpointParams['fields']
    endpointParams['access_token'] = params['access_token']

    url = params['endpoint_base'] + params['insta_acc_id']

    return makeApiCall(url, endpointParams, params['debug'])

def get_page_id(page_url, access_token):
    # Construct the API endpoint
    api_endpoint = f'https://graph.facebook.com/v18.0/?id={page_url}&fields=id&access_token={access_token}'

    try:
        # Make the API request
        response = requests.get(api_endpoint)
        response_data = response.json()

        # Check for errors in the response
        if 'error' in response_data:
            print(f"Error: {response_data['error']['message']}")
            return None

        # Extract the Page ID
        page_id = response_data.get('id')
        return page_id

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
def get_instagram_account_id(page_id, access_token):
    # Create the API endpoint
    api_endpoint = f'https://graph.facebook.com/v18.0/{page_id}?fields=instagram_business_account&access_token={access_token}'

    try:
        # Make the API request
        response = requests.get(api_endpoint)
        response_data = response.json()

        # Check for errors in the response
        if 'error' in response_data:
            print(f"Error: {response_data['error']['message']}")
            return None

        # Extract the Instagram Account ID
        instagram_account_id = response_data.get('instagram_business_account', {}).get('id')

        return instagram_account_id

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
