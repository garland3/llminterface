import os
import fnmatch
from pprint import pprint

def find_py_files(dir_path):
    py_files = []
    for root, dirs, files in os.walk(dir_path):
        for filename in fnmatch.filter(files, '*.py'):
            py_files.append(os.path.join(root, filename))
    return py_files

py_files = find_py_files('.')
pprint(py_files)
