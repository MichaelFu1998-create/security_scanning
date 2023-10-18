def __load_jams_schema():
    '''Load the schema file from the package.'''

    schema_file = os.path.join(SCHEMA_DIR, 'jams_schema.json')

    jams_schema = None
    with open(resource_filename(__name__, schema_file), mode='r') as fdesc:
        jams_schema = json.load(fdesc)

    if jams_schema is None:
        raise JamsError('Unable to load JAMS schema')

    return jams_schema