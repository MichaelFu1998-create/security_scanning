def dereference_package_descriptor(descriptor, base_path):
    """Dereference data package descriptor (IN-PLACE FOR NOW).
    """
    for resource in descriptor.get('resources', []):
        dereference_resource_descriptor(resource, base_path, descriptor)
    return descriptor