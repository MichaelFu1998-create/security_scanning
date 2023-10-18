def init_env():
    """
    Populates the global env variables with custom default settings.
    """
    env.ROLES_DIR = ROLE_DIR
    env.services = []
    env.confirm_deployment = False
    env.is_local = None
    env.base_config_dir = '.'
    env.src_dir = 'src' # The path relative to fab where the code resides.
    env.sites = {} # {site:site_settings}
    env[SITE] = None
    env[ROLE] = None

    env.hosts_retriever = None
    env.hosts_retrievers = type(env)() #'default':lambda hostname: hostname,

    env.hostname_translator = 'default'
    env.hostname_translators = type(env)()
    env.hostname_translators.default = lambda hostname: hostname

    env.default_site = None

    # A list of all site names that should be available on the current host.
    env.available_sites = []

    # A list of all site names per host.
    # {hostname: [sites]}
    # If no entry found, will use available_sites.
    env.available_sites_by_host = {}

    # The command run to determine the percent of disk usage.
    env.disk_usage_command = "df -H | grep -vE '^Filesystem|tmpfs|cdrom|none' | awk '{print $5 " " $1}'"

    env.burlap_data_dir = '.burlap'

    env.setdefault('roledefs', {})
    env.setdefault('roles', [])
    env.setdefault('hosts', [])
    env.setdefault('exclude_hosts', [])