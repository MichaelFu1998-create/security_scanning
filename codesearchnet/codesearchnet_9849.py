def dereference_resource_descriptor(descriptor, base_path, base_descriptor=None):
    """Dereference resource descriptor (IN-PLACE FOR NOW).
    """
    PROPERTIES = ['schema', 'dialect']
    if base_descriptor is None:
        base_descriptor = descriptor
    for property in PROPERTIES:
        value = descriptor.get(property)

        # URI -> No
        if not isinstance(value, six.string_types):
            continue

        # URI -> Pointer
        if value.startswith('#'):
            try:
                pointer = jsonpointer.JsonPointer(value[1:])
                descriptor[property] = pointer.resolve(base_descriptor)
            except Exception as error:
                message = 'Not resolved Pointer URI "%s" for resource.%s' % (value, property)
                six.raise_from(
                    exceptions.DataPackageException(message),
                    error
                )

        # URI -> Remote
        elif value.startswith('http'):
            try:
                response = requests.get(value)
                response.raise_for_status()
                descriptor[property] = response.json()
            except Exception as error:
                message = 'Not resolved Remote URI "%s" for resource.%s' % (value, property)
                six.raise_from(
                    exceptions.DataPackageException(message),
                    error
                )

        # URI -> Local
        else:
            if not is_safe_path(value):
                raise exceptions.DataPackageException(
                    'Not safe path in Local URI "%s" '
                    'for resource.%s' % (value, property))
            if not base_path:
                raise exceptions.DataPackageException(
                    'Local URI "%s" requires base path '
                    'for resource.%s' % (value, property))
            fullpath = os.path.join(base_path, value)
            try:
                with io.open(fullpath, encoding='utf-8') as file:
                    descriptor[property] = json.load(file)
            except Exception as error:
                message = 'Not resolved Local URI "%s" for resource.%s' % (value, property)
                six.raise_from(
                    exceptions.DataPackageException(message),
                    error
                )

    return descriptor