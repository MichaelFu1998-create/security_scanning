def licenses(self):
        ''' Return a list of licenses that apply to this module. (Strings,
            which may be SPDX identifiers)
        '''
        if 'license' in self.description:
            return [self.description['license']]
        else:
            return [x['type'] for x in self.description['licenses']]