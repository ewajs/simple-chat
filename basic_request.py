"""A handy module for making http requests. This should be deprecated when first version is released

"""
import requests


def get_from_server():
    r = requests.get('http://192.168.0.14:80')
    print(type(r))
    print(r.status_code)
    print(r.headers)
    print(r.headers['content-type'])
    print(r.text)


if __name__ == "__main__":
    get_from_server()