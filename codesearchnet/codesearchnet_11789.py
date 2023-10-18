def iter_sites(sites=None, site=None, renderer=None, setter=None, no_secure=False, verbose=None):
    """
    Iterates over sites, safely setting environment variables for each site.
    """
    if verbose is None:
        verbose = get_verbose()

    hostname = get_current_hostname()

    target_sites = env.available_sites_by_host.get(hostname, None)

    if sites is None:
        site = site or env.SITE or ALL
        if site == ALL:
            sites = list(six.iteritems(env.sites))
        else:
            sys.stderr.flush()
            sites = [(site, env.sites.get(site))]

    renderer = renderer #or render_remote_paths
    env_default = save_env()
    for _site, site_data in sorted(sites):
        if no_secure and _site.endswith('_secure'):
            continue

        # Only load site configurations that are allowed for this host.
        if target_sites is None:
            pass
        else:
            assert isinstance(target_sites, (tuple, list))
            if _site not in target_sites:
                if verbose:
                    print('Skipping site %s because not in among target sites.' % _site)
                continue

        env.update(env_default)
        env.update(env.sites.get(_site, {}))
        env.SITE = _site
        if callable(renderer):
            renderer()
        if setter:
            setter(_site)
        yield _site, site_data

    # Revert modified keys.
    env.update(env_default)

    # Remove keys that were added, not simply updated.
    added_keys = set(env).difference(env_default)
    for key in added_keys:
        # Don't remove internally maintained variables, because these are used to cache hostnames
        # used by iter_sites().
        if key.startswith('_'):
            continue
        del env[key]