import requests

def identify():
    return ["ip", "hash"]

def start(data_data, data_type):
    print("VT : Received : {} {}".format(data_data, data_type))
    return vtlookup(data_data)


def vtlookup(data_data):
    #r = requests.get()
    return 'vtlookup'