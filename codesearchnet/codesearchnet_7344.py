def get_authed_registries():
    """Reads the local Docker client config for the current user
    and returns all registries to which the user may be logged in.
    This is intended to be run client-side, not by the daemon."""
    result = set()
    if not os.path.exists(constants.DOCKER_CONFIG_PATH):
        return result
    config = json.load(open(constants.DOCKER_CONFIG_PATH, 'r'))
    for registry in config.get('auths', {}).iterkeys():
        try:
            parsed = urlparse(registry)
        except Exception:
            log_to_client('Error parsing registry {} from Docker config, will skip this registry').format(registry)
        # This logic assumes the auth is either of the form
        # gamechanger.io (no scheme, no path after host) or
        # of the form https://index.docker.io/v1/ (scheme,
        # netloc parses correctly, additional path does not matter).
        # These are the formats I saw in my personal config file,
        # not sure what other formats it might accept.
        result.add(parsed.netloc) if parsed.netloc else result.add(parsed.path)
    return result