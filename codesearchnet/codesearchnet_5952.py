def _gcp_client(project, mod_name, pkg_name, key_file=None, http_auth=None,
                user_agent=None):
    """
    Private GCP client builder.

    :param project: Google Cloud project string.
    :type project: ``str``

    :param mod_name: Module name to load.  Should be found in sys.path.
    :type mod_name: ``str``

    :param pkg_name: package name that mod_name is part of.  Default is 'google.cloud' .
    :type pkg_name: ``str``

    :param key_file: Default is None.
    :type key_file: ``str`` or None

    :param http_auth: httplib2 authorized client. Default is None.
    :type http_auth: :class: `HTTPLib2`

    :param user_agent: User Agent string to use in requests. Default is None.
    :type http_auth: ``str`` or None

    :return: GCP client
    :rtype: ``object``
    """
    client = None
    if http_auth is None:
        http_auth = _googleauth(key_file=key_file, user_agent=user_agent)
    try:
        # Using a relative path, so we prefix with a dot (.)
        google_module = importlib.import_module('.' + mod_name,
                                                package=pkg_name)
        client = google_module.Client(use_GAX=USE_GAX, project=project,
                                      http=http_auth)
    except ImportError as ie:
        import_err = 'Unable to import %s.%s' % (pkg_name, mod_name)
        raise ImportError(import_err)
    except TypeError:
        # Not all clients use gRPC
        client = google_module.Client(project=project, http=http_auth)
    if user_agent and hasattr(client, 'user_agent'):
        client.user_agent = user_agent
    return client