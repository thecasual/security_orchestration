import requests

def identify():
    return ["ip", "hash"]

def start(data_data, data_type, config):
    print("VT : Received : {} {}".format(data_data, data_type))
    return vtlookup(data_data, config['virustotalkey'])


def vtlookup(data_data, apikey):
    params = {'apikey' : apikey, 'resource': data_data}
    r = requests.get('https://www.virustotal.com/vtapi/v2/url/report', params = params)

    findings = {}
    cleanstatus = ['clean site', 'unrated site']

    if r.status_code == 200 and r.json()['verbose_msg'] == 'Scan finished, scan information embedded in this object':
        for scan in r.json()['scans']:
            if r.json()['scans'][scan]['result'] not in cleanstatus:
                findings[scan] = r.json()['scans'][scan]

    findings['hits'] = '{}/{}'.format(len(findings), len(r.json()['scans']))
    findings['permalink'] = r.json()['permalink']

    return findings