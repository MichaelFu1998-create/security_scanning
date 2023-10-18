def get_error(data):
    """ return the error if there is a corresponding exception """
    if isinstance(data, dict):
        if 'errors' in data:
            error = data['errors'][0]
        else:
            error = data.get('error', None)

        if isinstance(error, dict):
            if error.get('code') in errors:
                return error