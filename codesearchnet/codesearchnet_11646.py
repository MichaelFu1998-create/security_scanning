def createFromSource(cls, vs, name=None):
        ''' returns a git component for any git:// url, or None if this is not
            a git component.

            Normally version will be empty, unless the original url was of the
            form 'git://...#version', which can be used to grab a particular
            tag or branch, or ...#>=1.2.3, which can be used to specify
            semantic version specifications on tags.
        '''
        return GitComponent(vs.location, vs.spec, vs.semantic_spec)