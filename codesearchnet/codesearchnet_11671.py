def parseModuleNameAndSpec(module_name_and_spec):
    ''' Parse modulename[@versionspec] and return a tuple
        (module_name_string, version_spec_string).

        Also accepts raw github version specs (Owner/reponame#whatever), as the
        name can be deduced from these.

        Note that the specification split from the name is not validated. If
        there is no specification (just a module name) passed in, then '*' will
        be returned as the specification.
    '''
    import re
    # fist check if this is a raw github specification that we can get the
    # module name from:
    name, spec = _getNonRegistryRef(module_name_and_spec)
    if name:
        return name, module_name_and_spec

    # next split at the first @, if any
    name = module_name_and_spec.split('@')[0]
    spec = module_name_and_spec[len(name)+1:]

    name = name.strip()

    # if there's no specification, return the explicit any-version
    # specification:
    if not spec:
        spec = '*'

    return name, spec