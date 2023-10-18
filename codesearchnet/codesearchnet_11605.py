def createFromSource(cls, vs, name, registry):
        ''' returns a registry component for anything that's a valid package
            name (this does not guarantee that the component actually exists in
            the registry: use availableVersions() for that).
        '''
        # we deliberately allow only lowercase, hyphen, and (unfortunately)
        # numbers in package names, to reduce the possibility of confusingly
        # similar names: if the name doesn't match this then escalate to make
        # the user fix it. Targets also allow +
        if registry == 'targets':
            name_match = re.match('^[a-z]+[a-z0-9+-]*$', name)
            if not name_match:
                raise access_common.AccessException(
                    'Target name "%s" is not valid (must contain only lowercase letters, hyphen, plus, and numbers)' % name
                )
        else:
            name_match = re.match('^[a-z]+[a-z0-9-]*$', name)
            if not name_match:
                raise access_common.AccessException(
                    'Module name "%s" is not valid (must contain only lowercase letters, hyphen, and numbers)' % name
                )
        assert(vs.semantic_spec)
        return RegistryThing(name, vs.semantic_spec, registry)