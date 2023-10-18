def write_log(log_path, data, allow_append=True):
        """
        Writes the supplied specifications to the log path. The data
        may be supplied as either as a an Args or as a list of
        dictionaries.

        By default, specifications will be appropriately appended to
        an existing log file. This can be disabled by setting
        allow_append to False.
        """
        append = os.path.isfile(log_path)
        islist = isinstance(data, list)

        if append and not allow_append:
            raise Exception('Appending has been disabled'
                            ' and file %s exists' % log_path)

        if not (islist or isinstance(data, Args)):
            raise Exception('Can only write Args objects or dictionary'
                            ' lists to log file.')

        specs = data if islist else data.specs
        if not all(isinstance(el,dict) for el in specs):
            raise Exception('List elements must be dictionaries.')

        log_file = open(log_path, 'r+') if append else open(log_path, 'w')
        start = int(log_file.readlines()[-1].split()[0])+1 if append else 0
        ascending_indices = range(start, start+len(data))

        log_str = '\n'.join(['%d %s' % (tid, json.dumps(el))
                             for (tid, el) in zip(ascending_indices,specs)])
        log_file.write("\n"+log_str if append else log_str)
        log_file.close()