def expand_package_descriptor(descriptor):
    """Apply defaults to data package descriptor (IN-PLACE FOR NOW).
    """
    descriptor.setdefault('profile', config.DEFAULT_DATA_PACKAGE_PROFILE)
    for resource in descriptor.get('resources', []):
        expand_resource_descriptor(resource)
    return descriptor