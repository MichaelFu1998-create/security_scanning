def getDerivedTarget(
        target_name_and_version,
                   targets_path,
                application_dir = None,
                install_missing = True,
               update_installed = False,
              additional_config = None,
                     shrinkwrap = None
    ):
    # access, , get components, internal
    from yotta.lib import access
    from yotta.lib import access_common
    ''' Get the specified target description, optionally ensuring that it (and
        all dependencies) are installed in targets_path.

        Returns (DerivedTarget, errors), or (None, errors) if the leaf target
        could not be found/installed.
    '''
    logger.debug('satisfy target: %s' % target_name_and_version);
    if ',' in target_name_and_version:
        name, version_req = target_name_and_version.split(',')
    else:
        name = target_name_and_version
        version_req = '*'

    # shrinkwrap is the raw json form, not mapping form here, so rearrange it
    # before indexing:
    if shrinkwrap is not None:
        shrinkwrap_version_req = {
            x['name']: x['version'] for x in shrinkwrap.get('targets', [])
        }.get(name, None)
    else:
        shrinkwrap_version_req = None
    if shrinkwrap_version_req is not None:
        logger.debug(
            'respecting shrinkwrap version %s for %s', shrinkwrap_version_req, name
        )

    dspec = pack.DependencySpec(
                                 name,
                                 version_req,
        shrinkwrap_version_req = shrinkwrap_version_req
    )

    leaf_target      = None
    previous_name    = dspec.name
    search_dirs      = [targets_path]
    target_hierarchy = []
    errors           = []
    while True:
        t = None
        try:
            if install_missing:
                t = access.satisfyVersion(
                                 name = dspec.name,
                     version_required = dspec.versionReq(),
                            available = target_hierarchy,
                         search_paths = search_dirs,
                    working_directory = targets_path,
                     update_installed = ('Update' if update_installed else None),
                                 type = 'target',
                   inherit_shrinkwrap = shrinkwrap
                )
            else:
                t = access.satisfyVersionFromSearchPaths(
                                 name = dspec.name,
                     version_required = dspec.versionReq(),
                         search_paths = search_dirs,
                                 type = 'target',
                   inherit_shrinkwrap = shrinkwrap
                )
        except access_common.AccessException as e:
            errors.append(e)
        if not t:
            if install_missing:
                logger.error(
                    'could not install target %s for %s' %
                    (dspec, previous_name)
                )
            break
        else:
            target_hierarchy.append(t)
            previous_name = dspec.name
            assert(isinstance(t, Target))
            dspec = t.baseTargetSpec() #pylint: disable=no-member
            if not leaf_target:
                leaf_target = t
            if dspec is None:
                break
    if leaf_target is None:
        return (None, errors)
    # if we have a valid target, try to load the app-specific config data (if
    # any):
    app_config = {}
    if application_dir is not None:
        app_config_fname = os.path.join(application_dir, App_Config_File)
        if os.path.exists(app_config_fname):
            try:
                app_config = ordered_json.load(app_config_fname)
            except Exception as e:
                errors.append(Exception("Invalid application config.json: %s" % (e)))
    return (DerivedTarget(leaf_target, target_hierarchy[1:], app_config, additional_config), errors)