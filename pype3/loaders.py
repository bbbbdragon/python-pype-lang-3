import json

def dump_json(fileName,js):

    with open(fileName,'w') as f:

        f.write(json.dumps(js))


def load_json(fileName):

    with open(fileName,'r') as f:

        js=json.loads(f.read())

        return js
