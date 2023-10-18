def get_complete_version(version=None):
    """
    Returns a tuple of the django_cryptography version. If version
    argument is non-empty, then checks for correctness of the tuple
    provided.
    """
    if version is None:
        from django_cryptography import VERSION as version
    else:
        assert len(version) == 5
        assert version[3] in ('alpha', 'beta', 'rc', 'final')

    return version