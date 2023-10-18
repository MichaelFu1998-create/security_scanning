def get_dump_method(dump, protocol=-1):
    """Get dump function code string"""
    if dump is None:
        dump = 'pickle'
    if dump.startswith('pickle'):
        if dump == 'pickle':
            proto = protocol
        else:
            proto = dump.strip('pickle')
        try:
            proto = int(proto)
            assert proto>=-1
        except:
            raise Exception("protocol must be an integer >=-1")
        code = """
try:
    import cPickle as pickle
except:
    import pickle
with open('$FILE_PATH', 'wb') as fd:
    pickle.dump( value, fd, protocol=%i )
    fd.flush()
    os.fsync(fd.fileno())
"""%proto
    elif dump.startswith('dill'):
        if dump == 'dill':
            proto = 2
        else:
            proto = dump.strip('dill')
            try:
                proto = int(proto)
                assert proto>=-1
            except:
                raise Exception("protocol must be an integer >=-1")
        code = """
import dill
with open('$FILE_PATH', 'wb') as fd:
    dill.dump( value, fd, protocol=%i )
    fd.flush()
    os.fsync(fd.fileno())
"""%proto
    elif dump == 'json':
        code = """
import json
with open('$FILE_PATH', 'wb') as fd:
    json.dump( value,fd, ensure_ascii=True, indent=4 )
    fd.flush()
    os.fsync(fd.fileno())
"""
    elif dump == 'numpy':
        code = """
import numpy
with open('$FILE_PATH', 'wb') as fd:
    numpy.save(file=fd, arr=value)
    fd.flush()
    os.fsync(fd.fileno())
"""
    elif dump == 'numpy_text':
        code = """
import numpy
numpy.savetxt(fname='$FILE_PATH', X=value, fmt='%.6e')
"""
    else:
        assert isinstance(dump, basestring), "dump must be None or a string"
        assert '$FILE_PATH' in dump, "string dump code must inlcude '$FILE_PATH'"
        code = dump
    # return
    return code