def output(self, to=None, formatted=False, *args, **kwargs):
        '''Outputs the set text'''
        to.write('<!DOCTYPE {0}>'.format(self.type))