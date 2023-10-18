def get_descriptor_base_path(descriptor):
    """Get descriptor base path if string or return None.
    """

    # Infer from path/url
    if isinstance(descriptor, six.string_types):
        if os.path.exists(descriptor):
            base_path = os.path.dirname(os.path.abspath(descriptor))
        else:
            # suppose descriptor is a URL
            base_path = os.path.dirname(descriptor)

    # Current dir by default
    else:
        base_path = '.'

    return base_path