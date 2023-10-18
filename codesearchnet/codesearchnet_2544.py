def validated_formatter(self, url_format):
    """validate visualization url format"""
    # We try to create a string by substituting all known
    # parameters. If an unknown parameter is present, an error
    # will be thrown
    valid_parameters = {
        "${CLUSTER}": "cluster",
        "${ENVIRON}": "environ",
        "${TOPOLOGY}": "topology",
        "${ROLE}": "role",
        "${USER}": "user",
    }
    dummy_formatted_url = url_format
    for key, value in valid_parameters.items():
      dummy_formatted_url = dummy_formatted_url.replace(key, value)

    # All $ signs must have been replaced
    if '$' in dummy_formatted_url:
      raise Exception("Invalid viz.url.format: %s" % (url_format))

    # No error is thrown, so the format is valid.
    return url_format