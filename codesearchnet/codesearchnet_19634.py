def bump_version(version, which=None):
    """Returns the result of incrementing `version`.

    If `which` is not specified, the "patch" part of the version number will be
    incremented.  If `which` is specified, it must be ``'major'``, ``'minor'``,
    or ``'patch'``. If it is one of these three strings, the corresponding part
    of the version number will be incremented instead of the patch number.

    Returns a string representing the next version number.

    Example::

        >>> bump_version('2.7.1')
        '2.7.2'
        >>> bump_version('2.7.1', 'minor')
        '2.8.0'
        >>> bump_version('2.7.1', 'major')
        '3.0.0'

    """
    try:
        parts = [int(n) for n in version.split('.')]
    except ValueError:
        fail('Current version is not numeric')
    if len(parts) != 3:
        fail('Current version is not semantic versioning')
    # Determine where to increment the version number
    PARTS = {'major': 0, 'minor': 1, 'patch': 2}
    index = PARTS[which] if which in PARTS else 2
    # Increment the version number at that index and set the subsequent parts
    # to 0.
    before, middle, after = parts[:index], parts[index], parts[index + 1:]
    middle += 1
    return '.'.join(str(n) for n in before + [middle] + after)