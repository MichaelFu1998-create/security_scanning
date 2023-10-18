def getAdditionalIncludes(self):
        ''' Return the list of cmake files which are to be included by yotta in
            every module built. The list is returned in the order they should
            be included (most-derived last).
        '''
        return reversed([
            os.path.join(t.path, include_file)
                for t in self.hierarchy
                for include_file in t.description.get('cmakeIncludes', [])
        ])