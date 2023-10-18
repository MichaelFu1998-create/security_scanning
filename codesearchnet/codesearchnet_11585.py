def createFromSource(cls, vs, name=None):
        ''' returns a github component for any github url (including
            git+ssh:// git+http:// etc. or None if this is not a Github URL.
            For all of these we use the github api to grab a tarball, because
            that's faster.

            Normally version will be empty, unless the original url was of the
            form: 'owner/repo @version' or 'url://...#version', which can be used
            to grab a particular tagged version.

            (Note that for github components we ignore the component name - it
             doesn't have to match the github module name)
        '''
        return GithubComponent(vs.location, vs.spec, vs.semantic_spec, name)