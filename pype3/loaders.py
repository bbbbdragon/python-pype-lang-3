import json

def load_file_string(fileName):

    with open(fileName,'r') as f:

        return f.read()


def dump_json(fileName,js):

    with open(fileName,'w') as f:

        f.write(json.dumps(js))


def load_json(fileName):

    with open(fileName,'r') as f:

        js=json.loads(f.read())

        return js


def json_loads(jsonString):

    return json.loads(jsonString)

