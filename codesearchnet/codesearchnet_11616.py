def displayOutdated(modules, dependency_specs, use_colours):
    ''' print information about outdated modules,
        return 0 if there is nothing to be done and nonzero otherwise
    '''
    if use_colours:
        DIM    = colorama.Style.DIM       #pylint: disable=no-member
        NORMAL = colorama.Style.NORMAL    #pylint: disable=no-member
        BRIGHT = colorama.Style.BRIGHT    #pylint: disable=no-member
        YELLOW = colorama.Fore.YELLOW     #pylint: disable=no-member
        RED    = colorama.Fore.RED        #pylint: disable=no-member
        GREEN  = colorama.Fore.GREEN      #pylint: disable=no-member
        RESET  = colorama.Style.RESET_ALL #pylint: disable=no-member
    else:
        DIM = BRIGHT = YELLOW = RED = GREEN = RESET = u''

    status = 0

    # access, , get components, internal
    from yotta.lib import access
    from yotta.lib import access_common
    # sourceparse, , parse version source urls, internal
    from yotta.lib import sourceparse

    for name, m in modules.items():
        if m.isTestDependency():
            continue
        try:
            latest_v = access.latestSuitableVersion(name, '*', registry='modules', quiet=True)
        except access_common.Unavailable as e:
            latest_v = None

        if not m:
            m_version = u' ' + RESET + BRIGHT + RED + u"missing" + RESET
        else:
            m_version = DIM + u'@%s' % (m.version)
        if not latest_v:
            print(u'%s%s%s%s not available from the registry%s' % (RED, name, m_version, NORMAL, RESET))
            status = 2
            continue
        elif not m or m.version < latest_v:
            update_prevented_by = ''
            if m:
                specs_preventing_update = [
                    x for x in dependency_specs
                    if x.name == name and not
                       sourceparse.parseSourceURL(x.nonShrinkwrappedVersionReq()).semanticSpecMatches(latest_v)
                ]
                shrinkwrap_prevents_update = [
                    x for x in dependency_specs
                    if x.name == name and x.isShrinkwrapped() and not
                       sourceparse.parseSourceURL(x.versionReq()).semanticSpecMatches(latest_v)
                ]
                if len(specs_preventing_update):
                    update_prevented_by = ' (update prevented by specifications: %s)' % (
                        ', '.join(['%s from %s' % (x.version_req, x.specifying_module) for x in specs_preventing_update])
                    )
                if len(shrinkwrap_prevents_update):
                    update_prevented_by += ' yotta-shrinkwrap.json prevents update'
                if m.version.major() < latest_v.major():
                    # major versions being outdated might be deliberate, so not
                    # that bad:
                    colour = GREEN
                elif m.version.minor() < latest_v.minor():
                    # minor outdated versions is moderately bad
                    colour = YELLOW
                else:
                    # patch-outdated versions is really bad, because there should
                    # be no reason not to update:
                    colour = RED
            else:
                colour = RED
            print(u'%s%s%s latest: %s%s%s%s' % (name, m_version, RESET, colour, latest_v.version, update_prevented_by, RESET))
            if not status:
                status = 1
    return status