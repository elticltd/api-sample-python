import json
from main_functions import authenticate, retrieve_data, send_bulk_search_request

# python -m venv venv
# .\venv\Scripts\activate
# python.exe -m pip install --upgrade pip
# pip install requests

# Use the functions
account_token = "Email hello@eltic.io to get your token"
secret_key = "Email hello@eltic.io to get your secret key"

# Authenticate and get stateTokenKey
try:
    state_token_key, response_body = authenticate(account_token, secret_key)
    print("Authenticated. State Token Key:", state_token_key)
    
    # print the contents of the response as detail
    pretty_json = json.dumps(response_body.json()[0], indent=4)
    print(pretty_json)

except Exception as e:
    print(f"An error occurred during authentication: {str(e)}")


# Do a bulk search
            
# Step B1: Send a refresh request and retrieve the token
retrieve_token = None
try:
    # comment or uncomment the fields to perform the search on
    search_data = {
        "jobTitleList": "partner",
        # "professionList": "Solicitor",
        # "skillList": "Insurance",
        # "countryCode": "gb",
        # "locationList": "Manchester",
        # "openToWork": 1,
        # "hasEmail": 1,
        # "dateLastUpdated": "2024-01-01",
        "noOfRecordsRequested": 10
    }
    retrieve_token = send_bulk_search_request(state_token_key, search_data)
    print("Retrieve Token:", retrieve_token)

except Exception as e:
    print(f"Step B1: An error occurred: {str(e)}")

if retrieve_token:
    # Step B2: data is ready
    
    # Step B3: Retrieve the data because it is available
    try:
        data = retrieve_data(state_token_key, retrieve_token)

        # Iterate through all items in the response and print them, excluding 'jsonResult'
        for key, value in data.items():
            if key != 'jsonResult':
                print(f"{key}: {value}")

        # Extract and pretty print 'jsonResult' if it exists
        if 'jsonResult' in data:
            json_result = json.loads(data['jsonResult'])  # Parse 'jsonResult' as JSON
            pretty_json_result = json.dumps(json_result, indent=4)
            print(pretty_json_result)

    except Exception as e:
        print(f"Step B3: An error occurred: {str(e)}")