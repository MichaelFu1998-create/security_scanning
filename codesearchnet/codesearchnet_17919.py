def add_handler(self, name='console-color', level='info', formatter='standard', **kwargs):
        """
        Add another handler to the logging system if not present already.
        Available handlers are currently: ['console-bw', 'console-color', 'rotating-log']
        """
        # make sure the the log file has a name
        if name == 'rotating-log' and 'filename' not in kwargs:
            kwargs.update({'filename': self.logfilename})

        # make sure the the log file has a name
        if name == 'stringio' and 'stringio' not in kwargs:
            kwargs.update({'stringio': StringIO.StringIO()})

        handler = types[name](**kwargs)
        self.add_handler_raw(handler, name, level=level, formatter=formatter)