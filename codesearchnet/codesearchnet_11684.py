def _get_environ_handler(name, d):
    """
    Dynamically creates a Fabric task for each configuration role.
    """

    def func(site=None, **kwargs):
        from fabric import state

        # We can't auto-set default_site, because that break tasks that have
        # to operate over multiple sites.
        # If a task requires a site, it can pull from default_site as needed.
        #site = site or d.get('default_site') or env.SITE

        BURLAP_SHELL_PREFIX = int(os.environ.get('BURLAP_SHELL_PREFIX', '0'))
        if BURLAP_SHELL_PREFIX:
            print('#!/bin/bash')
            print('# Generated with:')
            print('#')
            print('#     export BURLAP_SHELL_PREFIX=1; export BURLAP_COMMAND_PREFIX=0; fab %s' % (' '.join(sys.argv[1:]),))
            print('#')

        BURLAP_COMMAND_PREFIX = int(os.environ.get('BURLAP_COMMAND_PREFIX', '1'))
        with_args = []
        if not BURLAP_COMMAND_PREFIX:
            for k in state.output:
                state.output[k] = False

        hostname = kwargs.get('hostname')
        hostname = hostname or kwargs.get('name')
        hostname = hostname or kwargs.get('hn')
        hostname = hostname or kwargs.get('h')

        verbose = int(kwargs.get('verbose', '0'))
        common.set_verbose(verbose)

        # Load environment for current role.
        env.update(env_default)
        env[common.ROLE] = os.environ[common.ROLE] = name
        if site:
            env[common.SITE] = os.environ[common.SITE] = site
        env.update(d)

        # Load host retriever.
        retriever = None
        if env.hosts_retriever:
            # Dynamically retrieve hosts.
#             module_name = '.'.join(env.hosts_retriever.split('.')[:-1])
#             func_name = env.hosts_retriever.split('.')[-1]
#             retriever = getattr(importlib.import_module(module_name), func_name)
            retriever = common.get_hosts_retriever()
            if verbose:
                print('Using retriever:', env.hosts_retriever, retriever)

        # Load host translator.
        translator = None
        if hostname:
            # Filter hosts list by a specific host name.
            module_name = '.'.join(env.hostname_translator.split('.')[:-1])
            func_name = env.hostname_translator.split('.')[-1]
            translator = getattr(importlib.import_module(module_name), func_name)

        # Re-load environment for current role, incase loading
        # the retriever/translator reset some environment values.
        env.update(env_default)
        env[common.ROLE] = os.environ[common.ROLE] = name
        if site:
            env[common.SITE] = os.environ[common.SITE] = site
        env.update(d)

        # Dynamically retrieve hosts.
        if env.hosts_retriever:
            if verbose:
                print('Building host list with retriever %s...' % env.hosts_retriever)
            env.hosts = list(retriever(site=site))
            if verbose:
                print('Found hosts:')
                print(env.hosts)

        # Filter hosts list by a specific host name.
        if hostname:
            _hostname = hostname
            hostname = translator(hostname=hostname)
            _hosts = env.hosts
            env.hosts = [_ for _ in env.hosts if _ == hostname]
            assert env.hosts, 'Hostname %s does not match any known hosts.' % (_hostname,)

        if env.is_local is None:
            if env.hosts:
                env.is_local = 'localhost' in env.hosts or '127.0.0.1' in env.hosts
            elif env.host_string:
                env.is_local = 'localhost' in env.host_string or '127.0.0.1' in env.host_string

        for cb in common.post_role_load_callbacks:
            cb()

        # Ensure satchels don't cache values from previously loaded roles.
        common.reset_all_satchels()

        if env.hosts and not env.host_string:
            env.host_string = env.hosts[0]

        if verbose:
            print('Loaded role %s.' % (name,), file=sys.stderr)

    func.__doc__ = 'Sets enivronment variables for the "%s" role.' % (name,)
    return func