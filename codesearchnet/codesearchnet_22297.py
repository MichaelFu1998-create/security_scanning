def amust(self, args, argv):
        '''
        Requires the User to provide a certain parameter
        for the method to function properly.
        Else, an Exception is raised.
        args - (tuple) arguments you are looking for.
        argv - (dict) arguments you have received and want to inspect.
        '''
        for arg in args:
            if str(arg) not in argv:
                raise KeyError("ArgMissing: " + str(arg) + " not passed")