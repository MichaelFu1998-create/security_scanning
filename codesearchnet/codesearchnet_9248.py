def validate_config(self):
        '''
        Validates the provided config to make sure all the required fields are 
        there.
        '''
        # first ensure that all the required fields are there
        for key, key_config in self.params_map.items():
            if key_config['required']:
                if key not in self.config:
                    raise ValueError("Invalid Configuration! Required parameter '%s' was not provided to Sultan.")
        
        # second ensure that the fields that were pased were actually fields that
        # can be used
        for key in self.config.keys():
            if key not in self.params_map:
                raise ValueError("Invalid Configuration! The parameter '%s' provided is not used by Sultan!" % key)