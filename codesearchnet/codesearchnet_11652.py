def getScript(self, scriptname):
        ''' return the specified script if one exists (possibly inherited from
            a base target)
        '''
        for t in self.hierarchy:
            s = t.getScript(scriptname)
            if s:
                return s
        return None