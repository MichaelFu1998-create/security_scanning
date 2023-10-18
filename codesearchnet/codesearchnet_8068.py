def get_params(self):
        '''Get the parameters for this object.  Returns as a dict.'''

        out = {}
        out['__class__'] = self.__class__
        out['params'] = dict(steps=[])

        for name, step in self.steps:
            out['params']['steps'].append([name, step.get_params(deep=True)])

        return out