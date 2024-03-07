#!/usr/bin/python3
""" Check response
"""
import requests

if __name__ == "__main__":
    """ Read user_id and session_id from file """
    session_id = "not a session ID"
    r = requests.get('http://0.0.0.0:5000/', cookies={ '_my_session_id': session_id })
    if r.status_code != 200:
        print("Wrong status code: {}".format(r.status_code))
        exit(1)
    if r.headers.get('content-type') != "application/json":
        print("Wrong content type: {}".format(r.headers.get('content-type')))
        exit(1)
    
    try:
        r_json = r.json()
        
        destroy_value = r_json.get('destroy')
        if destroy_value:
            print("destroy_session should return False if the session ID cookie sent is not linked to any user")
            exit(1)
            
        print("OK", end="")
    except:
        print("Error, not a JSON")
