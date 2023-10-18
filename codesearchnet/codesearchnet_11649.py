def loadAdditionalConfig(config_path):
    ''' returns (error, config)
    '''
    error = None
    config = {}
    if not config_path:
        return (error, config)
    if os.path.isfile(config_path):
        try:
            config = ordered_json.load(config_path)
        except Exception as e:
            error = "Invalid syntax in file %s: %s" % (config_path, e)
    else:
        # try to interpret the argument as literal JSON
        try:
            config = ordered_json.loads(config_path)
        except Exception as e:
            # if this fails too, guess whether it was intended to be JSON or
            # not, and display an appropriate error message
            if '{' in config_path or '}' in config_path:
                error = "Invalid syntax in literal JSON: %s" % e
            else:
                error = "File \"%s\" does not exist" % config_path
    logger.debug('read additional config: %s', config)
    return (error, config)