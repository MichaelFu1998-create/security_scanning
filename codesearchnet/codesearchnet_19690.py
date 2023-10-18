def _import_config(config_file):
    """returns a configuration object

    :param string config_file: path to config file
    """
    # get config file path
    jocker_lgr.debug('config file is: {0}'.format(config_file))
    # append to path for importing
    try:
        jocker_lgr.debug('importing config...')
        with open(config_file, 'r') as c:
            return yaml.safe_load(c.read())
    except IOError as ex:
        jocker_lgr.error(str(ex))
        raise RuntimeError('cannot access config file')
    except yaml.parser.ParserError as ex:
        jocker_lgr.error('invalid yaml file: {0}'.format(ex))
        raise RuntimeError('invalid yaml file')