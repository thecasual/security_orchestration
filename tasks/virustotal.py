import requests

def identify():
    return ["ip", "hash"]

def start(data):
    return vtlookup(data)


def vtlookup(data):
    r = requests.get()
    return 'vtlookup'