from posting import Posting
import httpx

def on_response(response: httpx.Response, posting: Posting) -> None:
    # Print the status code of the response to the log.
    if response.status_code == 200:

        token = response.json()["access_token"]
        
        print(token)
        posting.set_variable("auth_token", token)   
    # Set a variable to be used in later requests.
    # You can write '$auth_token' in the UI and it will be substituted with
    # the value of the $auth_token variable.
    #posting.set_variable("auth_token", response.headers["Authorization"])