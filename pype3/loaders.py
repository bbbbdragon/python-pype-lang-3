import json
import csv
import os
import chardet
import pickle

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


def load_bytes(fileName):

    with open(fileName,'rb') as f:

        text=f.read()
        encoding=chardet.detect(text)['encoding']
        text=text.decode(encoding)

        return text


def load_pickle(fileName):

    with open(fileName,'rb') as f:

        return pickle.load(f)


def os_listdir(dirName):

    return os.listdir(dirName)


def os_join(txt1,txt2):

    return os.path.join(txt1,txt2)


# def load_csv(fileName,delimiter=','):

    
