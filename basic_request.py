"""A handy module for making http requests. This should be deprecated when first version is released

"""
import requests
from datetime import datetime
import argparse

SERVER_HOST = 'localhost'

def get_from_server():
    r = requests.get(SERVER_HOST)
    print(type(r))
    print(r.status_code)
    print(r.headers)
    print(r.headers['content-type'])
    print(r.text)


def post_to_server():
    local_time = datetime.utcnow().replace(microsecond=0).isoformat()
    r = requests.post(f"http://{SERVER_HOST}/post_msg", 
                      json={"text": f"This is a test message delivered at {local_time}"})


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('server_host', metavar='S', type=str, 
                        help='the server hos or ip')
    parser.add_argument('method', metavar='M', type=str, 
                        help='the method for the request [POST, GET]')

    args = parser.parse_args()
    
    SERVER_HOST = args.server_host

    if args.method == 'POST':
        post_to_server()
    elif args.method == 'GET':
        get_from_server()