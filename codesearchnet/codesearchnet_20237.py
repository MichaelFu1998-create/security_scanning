def instantiate(repo, validator_name=None, filename=None, rulesfiles=None):
    """
    Instantiate the validation specification
    """

    default_validators = repo.options.get('validator', {})

    validators = {}
    if validator_name is not None:
        # Handle the case validator is specified..
        if validator_name in default_validators:
            validators = {
                validator_name : default_validators[validator_name]
            }
        else:
            validators = {
                validator_name : {
                    'files': [],
                    'rules': {},
                    'rules-files': []
                }
            }
    else:
        validators = default_validators

    #=========================================
    # Insert the file names
    #=========================================
    if filename is not None:
        matching_files = repo.find_matching_files([filename])
        if len(matching_files) == 0:
            print("Filename could not be found", filename)
            raise Exception("Invalid filename pattern")
        for v in validators:
            validators[v]['files'] = matching_files
    else:
        # Instantiate the files from the patterns specified
        for v in validators:
            if 'files' not in validators[v]:
                validators[v]['files'] = []
            elif len(validators[v]['files']) > 0:
                matching_files = repo.find_matching_files(validators[v]['files'])
                validators[v]['files'] = matching_files

    #=========================================
    # Insert the rules files..
    #=========================================
    if rulesfiles is not None:
        # Command lines...
        matching_files = repo.find_matching_files([rulesfiles])
        if len(matching_files) == 0:
            print("Could not find matching rules files ({}) for {}".format(rulesfiles,v))
            raise Exception("Invalid rules")
        for v in validators:
            validators[v]['rules-files'] = matching_files
    else:
        # Instantiate the files from the patterns specified
        for v in validators:
            if 'rules-files' not in validators[v]:
                validators[v]['rules-files'] = []
            else:
                rulesfiles = validators[v]['rules-files']
                matching_files = repo.find_matching_files(rulesfiles)
                validators[v]['rules-files'] = matching_files

    return validators