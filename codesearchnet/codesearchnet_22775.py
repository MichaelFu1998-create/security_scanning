def new_user(yaml_path):
    '''
    Return the consumer and oauth tokens with three-legged OAuth process and
    save in a yaml file in the user's home directory.
    '''

    print 'Retrieve API Key from https://www.shirts.io/accounts/api_console/'
    api_key = raw_input('Shirts.io API Key: ')

    tokens = {
        'api_key': api_key,
    }

    yaml_file = open(yaml_path, 'w+')
    yaml.dump(tokens, yaml_file, indent=2)
    yaml_file.close()

    return tokens