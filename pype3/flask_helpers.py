from flask import Flask, request, Response,jsonify
import requests
import json

def send_request(url,js):

    s=json.dumps(js)
    r=requests.post(url,data=s)
    rJS=json.loads(r.content)

    return rJS


