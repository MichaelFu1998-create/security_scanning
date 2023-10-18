def parseTargetNameAndSpec(target_name_and_spec):
    ''' Parse targetname[@versionspec] and return a tuple
        (target_name_string, version_spec_string).

        targetname[,versionspec] is also supported (this is how target names
        and specifications are stored internally, and was the documented way of
        setting the spec on the commandline)

        Also accepts raw github version specs (Owner/reponame#whatever), as the
        name can be deduced from these.

        Note that the specification split from the name is not validated. If
        there is no specification (just a target name) passed in, then '*' will
        be returned as the specification.
    '''
    import re
    # fist check if this is a raw github specification that we can get the
    # target name from:
    name, spec = _getNonRegistryRef(target_name_and_spec)
    if name:
        return name, target_name_and_spec

    # next split at the first @ or , if any
    split_at = '@'
    if target_name_and_spec.find('@') > target_name_and_spec.find(',') and \
            ',' in target_name_and_spec:
        split_at = ','
    name = target_name_and_spec.split(split_at)[0]
    spec = target_name_and_spec[len(name)+1:]

    name = name.strip()

    # if there's no specification, return the explicit any-version
    # specification:
    if not spec:
        spec = '*'

    return name, spec