def get_pull_method(pull):
    """Get pull function code string"""
    if pull is None or pull.startswith('pickle'):
        code = """
import os
try:
    import cPickle as pickle
except:
    import pickle
with open('$FILE_PATH', 'rb') as fd:
    PULLED_DATA = pickle.load( fd )
"""
    elif pull.startswith('dill'):
        code = """
import dill
with open('$FILE_PATH', 'rb') as fd:
    PULLED_DATA = dill.load( fd )
"""
    elif pull == 'json':
        code = """
import json
with open('$FILE_PATH', 'rb') as fd:
    PULLED_DATA = json.load(fd)
"""
    elif pull == 'numpy':
        code = """
import numpy
with open('$FILE_PATH', 'rb') as fd:
    PULLED_DATA=numpy.load(file=fd)

"""
    elif pull == 'numpy_text':
        code = """
import numpy
with open('$FILE_PATH', 'rb') as fd:
    PULLED_DATA=numpy.loadtxt(fname=fd)
"""
    else:
        assert isinstance(pull, basestring), "pull must be None or a string"
        assert 'PULLED_DATA' in pull, "string pull code must inlcude 'PULLED_DATA'"
        assert '$FILE_PATH' in pull, "string pull code must inlcude '$FILE_PATH'"
        code = pull
    # return
    return code