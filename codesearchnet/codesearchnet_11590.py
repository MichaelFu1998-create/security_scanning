def createFromSource(cls, vs, name=None):
        ''' returns a hg component for any hg:// url, or None if this is not
            a hg component.

            Normally version will be empty, unless the original url was of the
            form 'hg+ssh://...#version', which can be used to grab a particular
            tagged version.
        '''
        # strip hg of the url scheme:
        if vs.location.startswith('hg+'):
            location = vs.location[3:]
        else:
            location = vs.location
        return HGComponent(location, vs.spec)