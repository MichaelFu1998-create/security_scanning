def validate(self, descriptor):
        """https://github.com/frictionlessdata/datapackage-py#schema
        """

        # Collect errors
        errors = []
        for error in self._validator.iter_errors(descriptor):
            if isinstance(error, jsonschema.exceptions.ValidationError):
                message = str(error.message)
                if six.PY2:
                    message = message.replace('u\'', '\'')
                descriptor_path = '/'.join(map(str, error.path))
                profile_path = '/'.join(map(str, error.schema_path))
                error = exceptions.ValidationError(
                    'Descriptor validation error: %s '
                    'at "%s" in descriptor and '
                    'at "%s" in profile'
                    % (message, descriptor_path, profile_path))
            errors.append(error)

        # Raise error
        if errors:
            message = 'There are %s validation errors (see exception.errors)' % len(errors)
            raise exceptions.ValidationError(message, errors=errors)

        return True