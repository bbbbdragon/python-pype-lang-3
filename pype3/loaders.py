import json
import csv
import os
import chardet
import pickle
import numpy as np
from csv import DictReader

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


def load_utf(fileName):

    with open(fileName,'rb') as f:

        return f.read().decode('utf-8')


def load_pickle(fileName):

    with open(fileName,'rb') as f:

        return pickle.load(f)


def os_listdir(dirName):

    return os.listdir(dirName)


def os_basename(pth):

    return os.path.basename(pth)


def os_join(txt1,txt2):

    return os.path.join(txt1,txt2)


def os_is_file(path):

    return os.path.isfile(path)


def os_walk(path):

    return list(os.walk(path))


def os_walk_files(path,pattern=''):

    ls=[os_join(pth,fl) for pth,x,flLS in os.walk(path) for fl in flLS]
    ls=[pth for pth in ls if os_is_file(pth)]
    
    if not pattern:

        return ls

    return [pth for pth in ls if pattern in pth]


def os_path_split(dr):

    return os.path.split(dr)


def os_file(pth):

    return os_path_split(pth)[1]


def load_dir(dirName):

    files=[os_join(dirName,fl) for fl in os_listdir(dirName)]

    return {fl:load_bytes(fl) for fl in files}


def load_utf(fileName):

    with open(fileName,'rb') as f:

        return f.read().decode('utf-8',errors='replace')


def load_numpy(fileName):

    return np.load(fileName)


def load_csv(fileName):

    with open(fileName,'r') as f:

        return csv.reader(fileName)


def ordered_dct_to_dct(od):

    return {k:v for (k,v) in od.items()}


def load_csv_dct(fileName,delimiter=','):

    with open(fileName,'r') as f:

        cs=csv.DictReader(f,delimiter=delimiter)

        return [ordered_dct_to_dct(d) for d in cs]


def load_csv_dct_exception(fileName,delimiter=','):

    with open(fileName) as f:

        dctLS=[]
        dr=DictReader(f,delimiter=delimiter)

        for dct in dr:

            try:

                dctLS.append(dict(dct))

            except Exception as e:

                print(e)
                pass

        return dctLS

# def load_csv(fileName,delimiter=','):

    
