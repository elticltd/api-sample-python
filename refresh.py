import json
from main_functions import authenticate, send_refresh_request, check_if_data_ready, retrieve_data

# python -m venv venv
# .\venv\Scripts\activate
# python.exe -m pip install --upgrade pip
# pip install requests

# Use the functions
account_token = "Email hello@eltic.io to get your token"
secret_key = "Email hello@eltic.io to get your secret key"
vanity_name = "Choose a linkedin vanity name to test with"

# Authenticate and get stateTokenKey
try:
    state_token_key, response_body = authenticate(account_token, secret_key)
    print("Authenticated. State Token Key:", state_token_key)
    
    # print the contents of the response as detail
    pretty_json = json.dumps(response_body.json()[0], indent=4)
    print(pretty_json)

except Exception as e:
    print(f"An error occurred during authentication: {str(e)}")


# Do a refresh of a linkedin record

# Step A1: Send a refresh request and retrieve the token
try:
    retrieve_token = send_refresh_request(state_token_key, vanity_name)
    print("Retrieve Token:", retrieve_token)

except Exception as e:
    print(f"Step A1: An error occurred: {str(e)}")

if retrieve_token:
    # Step A2: Periodically check if data is ready
    try:
        data_ready_info = check_if_data_ready(state_token_key, retrieve_token)

        # Pretty print the JSON data
        pretty_json = json.dumps(data_ready_info, indent=4)
        print(pretty_json)

    except Exception as e:
        print(f"Step A2: An error occurred: {str(e)}")


    # Step A3: Retrieve the data because it is available
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
        print(f"Step A3: An error occurred: {str(e)}")