#!/usr/bin/python3
""" Check response
"""
import requests
import json

if __name__ == "__main__":
    user_id = None
    session_id = None
    
    """ Read user_id and session_id from file """
    with open("session_id_hbtn2.json", "r") as file:
        dJson = json.load(file)
        if dJson is None:
            dJson = {}
        user_id = dJson.get('user_id')
        session_id = dJson.get('session_id')

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
        if not destroy_value:
            print("destroy_session should return True if the session ID cookie sent is linked to a user")
            exit(1)
            
        print("OK", end="")
    except:
        print("Error, not a JSON")
