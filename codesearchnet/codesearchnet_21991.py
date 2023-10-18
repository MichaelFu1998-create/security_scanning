def validate(cls, definition):
        '''
        This static method validates a BioMapMapper definition.
        It returns None on success and throws an exception otherwise.
        '''
        schema_path = os.path.join(os.path.dirname(__file__),
                                   '../../schema/mapper_definition_schema.json')
        with open(schema_path, 'r') as jsonfp:
            schema = json.load(jsonfp)
        # Validation of JSON schema
        jsonschema.validate(definition, schema)
        # Validation of JSON properties relations
        assert definition['main_key'] in definition['supported_keys'], \
               '\'main_key\' must be contained in \'supported_keys\''
        assert set(definition.get('list_valued_keys', [])) <= set(definition['supported_keys']), \
               '\'list_valued_keys\' must be a subset of \'supported_keys\''
        assert set(definition.get('disjoint', [])) <= set(definition.get('list_valued_keys', [])), \
               '\'disjoint\' must be a subset of \'list_valued_keys\''
        assert set(definition.get('key_synonyms', {}).values()) <= set(definition['supported_keys']), \
               '\'The values of the \'key_synonyms\' mapping must be in \'supported_keys\''