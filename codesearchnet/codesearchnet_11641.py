def getExtraIncludes(self):
        ''' Some components must export whole directories full of headers into
            the search path. This is really really bad, and they shouldn't do
            it, but support is provided as a concession to compatibility.
        '''
        if 'extraIncludes' in self.description:
            return [os.path.normpath(x) for x in self.description['extraIncludes']]
        else:
            return []