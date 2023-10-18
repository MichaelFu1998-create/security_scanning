def output(self, to=None, *args, **kwargs):
        '''Outputs the set text'''
        to.write(str(self._value))