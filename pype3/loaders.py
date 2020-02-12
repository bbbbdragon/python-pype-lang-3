import json
import csv
def dump_json(fileName,js):

    with open(fileName,'w') as f:

        f.write(json.dumps(js))


def load_list_file(fileName):

    with open(fileName,'r') as f:

        return [ln for ln in f.read().splitlines()]


def load_json(fileName):

    with open(fileName,'r') as f:

        js=json.loads(f.read())

        return js


# def load_csv(fileName,delimiter=','):

    
