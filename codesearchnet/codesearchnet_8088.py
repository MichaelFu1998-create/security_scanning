def init(args):
    """Initialize or edit an existing .osfcli.config file."""
    # reading existing config file, convert to configparser object
    config = config_from_file()
    config_ = configparser.ConfigParser()
    config_.add_section('osf')
    if 'username' not in config.keys():
        config_.set('osf', 'username', '')
    else:
        config_.set('osf', 'username', config['username'])
    if 'project' not in config.keys():
        config_.set('osf', 'project', '')
    else:
        config_.set('osf', 'project', config['project'])

    # now we can start asking for new values
    print('Provide a username for the config file [current username: {}]:'.format(
          config_.get('osf', 'username')))
    username = input()
    if username:
        config_.set('osf', 'username', username)

    print('Provide a project for the config file [current project: {}]:'.format(
          config_.get('osf', 'project')))
    project = input()
    if project:
        config_.set('osf', 'project', project)

    cfgfile = open(".osfcli.config", "w")
    config_.write(cfgfile)
    cfgfile.close()