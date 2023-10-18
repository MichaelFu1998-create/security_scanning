def retrieve_descriptor(descriptor):
    """Retrieve descriptor.
    """
    the_descriptor = descriptor

    if the_descriptor is None:
        the_descriptor = {}

    if isinstance(the_descriptor, six.string_types):
        try:
            if os.path.isfile(the_descriptor):
                with open(the_descriptor, 'r') as f:
                    the_descriptor = json.load(f)
            else:
                req = requests.get(the_descriptor)
                req.raise_for_status()
                # Force UTF8 encoding for 'text/plain' sources
                req.encoding = 'utf8'
                the_descriptor = req.json()
        except (IOError, requests.exceptions.RequestException) as error:
            message = 'Unable to load JSON at "%s"' % descriptor
            six.raise_from(exceptions.DataPackageException(message), error)
        except ValueError as error:
            # Python2 doesn't have json.JSONDecodeError (use ValueErorr)
            message = 'Unable to parse JSON at "%s". %s' % (descriptor, error)
            six.raise_from(exceptions.DataPackageException(message), error)

    if hasattr(the_descriptor, 'read'):
        try:
            the_descriptor = json.load(the_descriptor)
        except ValueError as e:
            six.raise_from(exceptions.DataPackageException(str(e)), e)

    if not isinstance(the_descriptor, dict):
        msg = 'Data must be a \'dict\', but was a \'{0}\''
        raise exceptions.DataPackageException(msg.format(type(the_descriptor).__name__))

    return the_descriptor