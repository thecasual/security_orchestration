import importlib
import tasks
import argparse
import json
import pkgutil
import re
from case import *

def iter_namespace(ns_pkg):
    # Specifying the second argument (prefix) to iter_modules makes the
    # returned name an absolute name instead of a relative one. This allows
    # import_module to work without having to do additional modification to
    # the name.
    return pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + ".")

def gettasks():
    t = {
        name: importlib.import_module(name)
        for finder, name, ispkg in iter_namespace(tasks)
    }
    # format of hashmap like  {'outputplugins.stdout': <module 'outputplugins.stdout' from '/path/outputplugins/stdout.py'>}
    return t

def parseparams():

    desc = 'Security Orchestration'
    epilog = "Automate all the things"
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, description=desc,epilog=epilog)
    parser.add_argument("--type", "-t", help="Force a data type : ip, domain, hash")
    parser.add_argument("--data", "-d", help="Example : 1.1.1.1")
    parser.add_argument("--case", "-c", help="open, close")
    args = parser.parse_args()
    
    return args

def parsedata(data):
    domainregex = re.compile("(^[\d\w-]+\.[\d\w]+$)")
    hashregex = re.compile("(^[A-Fa-f0-9]{64}$)")
    ipregex = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")

    print("Parsing {}".format(data))

    if domainregex.match(data):
        return 'domain'
    elif hashregex.match(data):
        return 'hash'
    elif ipregex.match(data):
        return 'ip'
    else:
        return 'None'

if __name__ == "__main__":

    configfile = r'orchestration.conf'
    secrets = r'secrets.conf'

    with open(configfile) as config:
        config = json.load(config)

    with open(secrets) as s:
        secret = json.load(s)

    # flat

    config = {**secret, **config}


    params = parseparams()

    tasks_all = gettasks()

    tasks = {}
    for task in tasks_all:
        if tasks_all[task].identify():
            tasks_all[task] = tasks_all[task].identify()

    print("Tasks : {}".format(tasks_all))

    if params.data and params.type:
        print("Data : {} Type : {}".format(params.data, params.type))

    elif not params.type and params.data:
        print("Type not provided...parsing data {}".format(params.data))
        params.type = parsedata(params.data)
        print(params.type)

    if params.type != 'None':
        task_run = []
        for t in tasks_all:
            if params.type in tasks_all[t]:
                task_run.append(t)
    else:
        exit()


    # Run applicable task

    case = casemgmt()
    case.collection = {}

    if params.case == 'open':
        case.status = params.case

    print(task_run)

    for run in task_run:
        py_run = importlib.import_module(run)
        print("Sending parameter {}".format(params.type))
        case.collection[run] = py_run.start(params.data, params.type, config)

    print(case.collection)