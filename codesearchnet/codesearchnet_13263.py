def validate(schema_file=None, jams_files=None):
    '''Validate a jams file against a schema'''

    schema = load_json(schema_file)

    for jams_file in jams_files:
        try:
            jams = load_json(jams_file)
            jsonschema.validate(jams, schema)
            print '{:s} was successfully validated'.format(jams_file)
        except jsonschema.ValidationError as exc:
            print '{:s} was NOT successfully validated'.format(jams_file)

            print exc