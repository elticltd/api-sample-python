# api-sample-python
Sample Python script to demonstrate how to implement the ELTic API

**Refer to the API document to get the details of the API.  This details the example implementation scripts.**

## Note:
### Request your account by emailing your details to hello@eltic.io
- account_token = "Email hello@eltic.io to get your token"
- secret_key = "Email hello@eltic.io to get your secret key"
- vanity_name = "Choose a linkedin vanity name to test with"*

*See section below explaining the vanity name


## Files
- main_functions contains all the referenced functions to call.  The api calls are managed within each of the functions for example purposes.
- refresh is the example to do a refresh of a person.
- bulksearch contains an example to do a bulk search.


## Sequence of function calls in the application
1. Authenticate with the authenticate function.
2. Send a refresh request using send_refresh_request.
3. Check periodically if the data is ready using check_if_data_ready.
4. Once data is ready, retrieve it using retrieve_data.


## 1. authenticate(account_token, secret_key)

Purpose: This function is used to authenticate against the API. It sends the accountToken and secretKey to the API's login endpoint.

**How it works:**

- It makes a POST request to the API's login endpoint.
- On successful authentication, the API returns a response header containing statetokenkey, which is necessary for subsequent API requests.
- If authentication fails, it raises an exception with the failure reason.

**Usage:**
```
try:
    state_token_key, response = authenticate(your_account_token, your_secret_key)
except Exception as e:
    print(f"Authentication failed: {str(e)}")
```


## 2. send_refresh_request(state_token_key, vanity_name)

Purpose: To initiate a data refresh request.

**How it works:**

- It takes the authenticated state_token_key and a vanity_name as parameters.
- It sends a GET request to the API's refresh endpoint.
- Upon success, it returns a RetrieveToken, which is used in subsequent data retrieval.

**Usage:**
```
try:
    retrieve_token = send_refresh_request(state_token_key, vanity_name)
except Exception as e:
    print(f"Failed to send refresh request: {str(e)}")
```


## 3. check_if_data_ready(state_token_key, retrieve_token, timeout)

Purpose: Periodically checks if the refreshed data is ready for retrieval.

**How it works:**

- It repeatedly makes GET requests to the API's availability check endpoint until the data is ready, or a timeout occurs.
- It uses the retrieve_token obtained from the refresh request.
- If data is ready (IsJsonReady is 1), it returns the ready data's metadata. If the data is not ready within the specified timeout, it raises an exception.

**Usage:**
```
try:
    data_ready_info = check_if_data_ready(state_token_key, retrieve_token)
except Exception as e:
    print(f"Error in data readiness check: {str(e)}")
```


## 4. retrieve_data(state_token_key, retrieve_token)

Purpose: To retrieve the data once it's ready.

**How it works:**

It sends a GET request to the API's data retrieval endpoint using the retrieve_token.
If successful, it returns the retrieved data.
In case of errors (like insufficient credits, HTTP errors, or JSON decoding errors), it raises appropriate exceptions.

**Usage:**
```
try:
    retrieved_data = retrieve_data(state_token_key, retrieve_token)
    # Process the retrieved_data as needed
except Exception as e:
    print(f"Data retrieval failed: {str(e)}")
```


## Note:

- **The state_token_key obtained from authentication is crucial and used in all subsequent API requests.**
- Handle exceptions at each stage to ensure robust error handling.
- Ensure you have proper sleep or wait times in the check_if_data_ready function to avoid excessive API calls.
- This sequence provides a complete workflow for interacting with the API, from authentication to data retrieval.


## vanity name

A "vanity name" on LinkedIn refers to a customizable part of your LinkedIn profile URL, usually representing your name or a variation of it, making it easy to remember and share. 

This personalized URL typically follows the format of **linkedin.com/in/[vanityname]**.

### Short Description:

A LinkedIn vanity name is a user-defined, unique identifier in your LinkedIn profile URL.
It helps create a more professional and memorable LinkedIn URL instead of a URL with a series of random numbers and letters.
It's often used for personal branding and makes it easier for others to find and connect with you on LinkedIn.


### Example of a Vanity Name:

Suppose your name is John Doe. A LinkedIn profile URL with a vanity name could be:

  https://www.linkedin.com/in/johndoe

  https://www.linkedin.com/in/john-doe

In this case, "johndoe" or "john-doe" is the vanity name. It's a simple, professional way to represent yourself on LinkedIn.

## Disclaimer
Please use this responsibly.  This is not inteded to be production ready or secure to be used on a production environment.  The purpose is to provide an example of how these calls works using Python.
