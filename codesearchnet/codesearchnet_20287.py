def init(globalvars=None, show=False):
    """
    Load profile INI
    """
    global config

    profileini = getprofileini()
    if os.path.exists(profileini):
        config = configparser.ConfigParser()
        config.read(profileini)
        mgr = plugins_get_mgr()
        mgr.update_configs(config)

        if show:
            for source in config:
                print("[%s] :" %(source))
                for k in config[source]:
                    print("   %s : %s" % (k, config[source][k]))

    else:
        print("Profile does not exist. So creating one")
        if not show:
            update(globalvars)

    print("Complete init")