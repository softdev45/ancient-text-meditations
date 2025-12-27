import requests
from ancient_texts.greek_gospel import *


from flask import Flask, jsonify, request

# The target URL for the server's endpoint
SERVER_ENDPOINT_WORD = "http://127.0.0.1:5001/related_words"
SERVER_ENDPOINT_VERSE = "http://127.0.0.1:5001/verse"

lib = None

def greek_search_word(search_phrase):
    global lib
    if not lib:
        lib = build_books_lib()
    return lib.search(search_phrase)

def greek_verse(ref):
    global lib
    if not lib:
        lib = build_books_lib()
    return lib.get_ref(ref[0], ref[1], ref[2])


def get_verse(ref):
    # payload = {
    #     "loc": word
    # }

    # # 2. Define the headers, specifying that the body is JSON
    # headers = {
    #     "Content-Type": "application/json"
    # }
    suff = f"?ref={ref}"


    # 3. Make the POST request using the 'requests' library
    try:
        # requests.post sends the HTTP request
        # response = requests.post(SERVER_ENDPOINT, json=payload, headers=headers, timeout=5)
        response = requests.get(SERVER_ENDPOINT_VERSE+suff, timeout=5)
        
        # 4. Check if the request was successful (HTTP status code 200)
        if response.status_code == 200:
            # 5. Extract the JSON response from the server
            server_data = response.json()
            print(server_data)
            return server_data
            
            # Return the server's data back to the original client request
            # return jsonify({
            # return server_data
        else:
            # Handle non-200 status codes (e.g., 400, 404, 500)
            return None
    except:
      return None


# @app.route('/trigger_request/<word>', methods=['GET'])
def trigger_request(word, lang="ToC"):
    """
    This client endpoint makes a POST request to the separate Flask server.
    
    Args:
        word: The word to send to the server, provided as a path parameter.
    """
    print(f"Client: Attempting to send '{word}' to the server at {SERVER_ENDPOINT_WORD}...")
    
    # 1. Define the JSON payload required by the server
    payload = {
        "input_word": word,
        "lang": lang
    }

    # 2. Define the headers, specifying that the body is JSON
    headers = {
        "Content-Type": "application/json"
    }

    # 3. Make the POST request using the 'requests' library
    try:
        # requests.post sends the HTTP request
        response = requests.post(SERVER_ENDPOINT_WORD, json=payload, headers=headers, timeout=5)
        
        # 4. Check if the request was successful (HTTP status code 200)
        if response.status_code == 200:
            # 5. Extract the JSON response from the server
            server_data = response.json()
            return server_data
            
            # Return the server's data back to the original client request
            # return jsonify({
            return ({
                "status": "success",
                "message": f"Successfully received data from the server for word '{word}'.",
                "server_response": server_data
            })
        else:
            # Handle non-200 status codes (e.g., 400, 404, 500)
            return jsonify({
                "status": "error",
                "message": f"Server returned status code {response.status_code}",
                "server_details": response.text
            }), response.status_code

    except requests.exceptions.ConnectionError:
        return jsonify({
            "status": "error",
            "message": f"Could not connect to the server at {SERVER_ENDPOINT_WORD}. Is the server running?"
        }), 503
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"An unexpected error occurred: {str(e)}"
        }), 500