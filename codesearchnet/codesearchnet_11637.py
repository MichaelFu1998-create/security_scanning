def getTarget(self, target_name_and_version, additional_config=None):
        ''' Return a derived target object representing the selected target: if
            the target is not installed, or is invalid then the returned object
            will test false in a boolean context.

            Returns derived_target

            Errors are not displayed.
        '''
        derived_target, errors = self.satisfyTarget(
                               target_name_and_version,
           additional_config = additional_config,
             install_missing = False
        )
        if len(errors):
            return None
        else:
            return derived_target