def update(globalvars):
    """
    Update the profile
    """
    global config

    profileini = getprofileini()
    config = configparser.ConfigParser()
    config.read(profileini)
    defaults = {}

    if globalvars is not None:
        defaults = {a[0]: a[1] for a in globalvars }

    # Generic variables to be captured...
    generic_configs = [{
        'name': 'User',
        'nature': 'generic',
        'description': "General information",
        'variables': ['user.email', 'user.name',
                      'user.fullname'],
        'defaults': {
            'user.email': {
                'value': defaults.get('user.email',''),
                'description': "Email address",
                'validator': EmailValidator()
            },
            'user.fullname': {
                'value': defaults.get('user.fullname',''),
                'description': "Full Name",
                'validator': NonEmptyValidator()
            },
            'user.name': {
                'value': defaults.get('user.name', getpass.getuser()),
                'description': "Name",
                'validator': NonEmptyValidator()
            },
        }
    }]

    # Gather configuration requirements from all plugins
    mgr = plugins_get_mgr()
    extra_configs = mgr.gather_configs()
    allconfigs = generic_configs + extra_configs

    # Read the existing config and update the defaults
    for c in allconfigs:
        name = c['name']
        for v in c['variables']:
            try:
                c['defaults'][v]['value'] = config[name][v]
            except:
                continue

    for c in allconfigs:

        print("")
        print(c['description'])
        print("==================")
        if len(c['variables']) == 0:
            print("Nothing to do. Enabled by default")
            continue

        name = c['name']
        config[name] = {}
        config[name]['nature'] = c['nature']
        for v in c['variables']:

            # defaults
            value = ''
            description = v + " "
            helptext = ""
            validator = None

            # Look up pre-set values
            if v in c['defaults']:
                value = c['defaults'][v].get('value','')
                helptext = c['defaults'][v].get("description","")
                validator = c['defaults'][v].get('validator',None)
            if helptext != "":
                description += "(" + helptext + ")"

            # Get user input..
            while True:
                choice = input_with_default(description, value)
                if validator is not None:
                    if validator.is_valid(choice):
                        break
                    else:
                        print("Invalid input. Expected input is {}".format(validator.message))
                else:
                    break

            config[name][v] = choice

            if v == 'enable' and choice == 'n': 
                break 

    with open(profileini, 'w') as fd:
        config.write(fd)

    print("Updated profile file:", config)