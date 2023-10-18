def checkDependenciesForShrinkwrap(dependency_list):
    ''' return a list of errors encountered (e.g. dependency missing or
        specification not met
    '''
    # sourceparse, , parse version specifications, internall
    from yotta.lib import sourceparse
    errors = []
    # first gather the available versions of things:
    available_versions = {}
    for mod in dependency_list.get('modules', []):
        available_versions[mod['name']] = mod['version']
    # now check that the available versions satisfy all of the specifications
    # from other modules:
    for mod in dependency_list.get('modules', []):
        for spec_info in mod.get('specifications', []):
            name = spec_info['name']
            spec = spec_info['version']
            if spec_info.get('testOnly', False):
                # test-only specifications are ignored for shrinkwrap
                continue
            if not name in available_versions:
                errors.append('dependency %s (required by %s) is missing' % (
                    name, mod['name']
                ))
            else:
                available_version = available_versions[name]
                parsed_spec = sourceparse.parseSourceURL(spec)
                if not parsed_spec.semanticSpecMatches(available_version):
                    errors.append('%s@%s does not meet specification %s required by %s' % (
                        name, available_version, parsed_spec.semanticSpec(), mod['name']
                    ))

    return errors