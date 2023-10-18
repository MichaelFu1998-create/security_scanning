def call(self, this, args=()):
        ''' Dont use this method from inside bytecode to call other bytecode. '''
        if self.is_native:
            _args = SpaceTuple(
                args
            )  # we have to do that unfortunately to pass all the necessary info to the funcs
            _args.space = self.space
            return self.code(
                this, _args
            )  # must return valid js object - undefined, null, float, unicode, bool, or PyJs
        else:
            return self.space.exe._call(self, this,
                                        args)