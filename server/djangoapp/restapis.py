# Uncomment the imports below before you add the function code
import requests
import os
from dotenv import load_dotenv

load_dotenv()

backend_url = os.getenv('backend_url', default="http://localhost:3030")
sentiment_analyzer_url = os.getenv(
    'sentiment_analyzer_url', default="http://localhost:5050/"
)


# Add code for get requests to back end
def get_request(endpoint, **kwargs):
    params = ""
    if kwargs:
        for key, value in kwargs.items():
            params = params + key + "=" + value + "&"

    request_url = backend_url + endpoint + "?" + params
    print("GET from {} ".format(request_url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(request_url)
        return response.json()
    except Exception as e:
        # If any error occurs
        print("Network exception occurred:", e)


# Add code for retrieving sentiments
def analyze_review_sentiments(text):
    request_url = sentiment_analyzer_url + "analyze/" + text
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(request_url)
        return response.json()
    except Exception as err:
        print(f"Unexpected error: {err}")
        print("Network exception occurred")


# Add code for posting review with debugging statements
def post_review(data_dict):
    request_url = backend_url + "/insert_review"
    print("Request URL:", request_url)
    print("Data being sent:", data_dict)

    try:
        # Make the POST request with the provided JSON data
        response = requests.post(request_url, json=data_dict)
        print("Status Code:", response.status_code)

        # Check if response status code is not successful
        if response.status_code != 200:
            print("Error in response:", response.text)
            return {"status": "error", "message": response.text}

        # Try to parse the response as JSON
        try:
            response_data = response.json()
            print("Response Data:", response_data)  # Print the JSON response
            return response_data
        except ValueError:
            # If response isn't JSON, return the text response
            print("Response is not JSON:", response.text)
            return {
                "status": "error",
                "message": "Invalid JSON response",
                "data": response.text,
            }

    except requests.exceptions.RequestException as e:
        # Handle network-related errors (connection, timeout, etc.)
        print("Network exception occurred:", e)
        return {"status": "error", "message": str(e)}
    except Exception as e:
        # Catch any other unforeseen errors
        print("Unexpected error occurred:", e)
        return {"status": "error", "message": str(e)}
