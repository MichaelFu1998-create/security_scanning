def parallel_concat_worker(task):
    '''
    This is a worker for the function below.

    task[0] = lcbasedir
    task[1] = objectid
    task[2] = {'aperture','postfix','sortby','normalize','outdir','recursive'}

    '''

    lcbasedir, objectid, kwargs = task

    try:
        return concat_write_pklc(lcbasedir, objectid, **kwargs)
    except Exception as e:
        LOGEXCEPTION('failed LC concatenation for %s in %s'
                     % (objectid, lcbasedir))
        return None