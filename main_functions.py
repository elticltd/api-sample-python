import requests
import time

def authenticate(account_token, secret_key):
    url = "https://api.eltic.io/api/accountlogin"
    data = {
        "accountToken": account_token,
        "secretKey": secret_key
    }
    response = requests.post(url, json=data)
    if response.status_code == 200:
        if 'statetokenkey' in response.headers:
            return response.headers['statetokenkey'], response
        else:
            raise Exception("stateTokenKey not found in response headers")
    else:
        raise Exception("Authentication Failed: " + response.text)


def send_refresh_request(state_token_key, vanity_name):
    url = f"https://api.eltic.io/api/refresh?vanityName={vanity_name}"
    headers = {
        "charset": "UTF-8",
        "content-type": "application/json",
        "accept": "application/json",
        "statetokenkey": state_token_key
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises HTTPError for bad HTTP status codes
        try:
            return response.json()[0]['RetrieveToken']
        except (IndexError, KeyError, ValueError):
            raise ValueError("Invalid JSON response format or missing 'RetrieveToken'")
    except requests.RequestException as e:
        raise Exception(f"Network or HTTP error occurred: {e}")
    
def send_bulk_request(state_token_key, vanity_name):
    url = f"https://api.eltic.io/api/bulksearch?vanityName={vanity_name}"
    headers = {
        "charset": "UTF-8",
        "content-type": "application/json",
        "accept": "application/json",
        "statetokenkey": state_token_key
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises HTTPError for bad HTTP status codes
        try:
            return response.json()[0]['RetrieveToken']
        except (IndexError, KeyError, ValueError):
            raise ValueError("Invalid JSON response format or missing 'RetrieveToken'")
    except requests.RequestException as e:
        raise Exception(f"Network or HTTP error occurred: {e}")


def check_if_data_ready(state_token_key, retrieve_token, timeout=600):
    url = f"https://api.eltic.io/api/available?retrievetoken={retrieve_token}"
    headers = {
        "charset": "UTF-8",
        "content-type": "application/json",
        "accept": "application/json",
        "statetokenkey": state_token_key
    }
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                response_json = response.json()[0]
                if response_json['IsJsonReady'] == 1:
                    return response_json  # Success
            else:
                raise Exception(f"Error: status_code: {response.status_code}, response: {response.text}")
        except requests.RequestException as e:
            raise Exception(f"Error: Network-related error occurred - {str(e)}")
        time.sleep(15)
    raise Exception("Error: Data was not ready after 10 minutes.")


def retrieve_data(state_token_key, retrieve_token):
    url = f"https://api.eltic.io/api/retrieve?retrievetoken={retrieve_token}"
    headers = {
        "charset": "UTF-8",
        "content-type": "application/json",
        "accept": "application/json",
        "statetokenkey": state_token_key
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises an HTTPError for bad HTTP status codes
        
        if response.status_code == 204:
            raise ValueError("Not enough credit to retrieve the data. Buy more credit and then attempt the retrieve again.")
        
        try:
                return response.json()[0]
        except (IndexError, KeyError, ValueError):
            raise ValueError("Invalid JSON response format or missing expected data.")
    except requests.RequestException as e:
        raise Exception(f"Network or HTTP error occurred: {e}")
    

def send_bulk_search_request(state_token_key, data):
    url = "https://api.eltic.io/api/bulksearch"
    headers = {
        "charset": "UTF-8",
        "content-type": "application/json",
        "accept": "application/json",
        "statetokenkey": state_token_key
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Raises an HTTPError for bad HTTP status codes

        try:
            return response.json()[0]['RetrieveToken']
        except ValueError:
            raise ValueError("Invalid JSON response format or missing expected data.")
    except requests.RequestException as e:
        raise Exception(f"Network or HTTP error occurred: {e}")

