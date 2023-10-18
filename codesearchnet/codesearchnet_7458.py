def get_newest_possible_languagetool_version():
    """Return newest compatible version.

    >>> version = get_newest_possible_languagetool_version()
    >>> version in [JAVA_6_COMPATIBLE_VERSION,
    ...             JAVA_7_COMPATIBLE_VERSION,
    ...             LATEST_VERSION]
    True

    """
    java_path = find_executable('java')
    if not java_path:
        # Just ignore this and assume an old version of Java. It might not be
        # found because of a PATHEXT-related issue
        # (https://bugs.python.org/issue2200).
        return JAVA_6_COMPATIBLE_VERSION

    output = subprocess.check_output([java_path, '-version'],
                                     stderr=subprocess.STDOUT,
                                     universal_newlines=True)

    java_version = parse_java_version(output)

    if java_version >= (1, 8):
        return LATEST_VERSION
    elif java_version >= (1, 7):
        return JAVA_7_COMPATIBLE_VERSION
    elif java_version >= (1, 6):
        warn('language-check would be able to use a newer version of '
             'LanguageTool if you had Java 7 or newer installed')
        return JAVA_6_COMPATIBLE_VERSION
    else:
        raise SystemExit(
            'You need at least Java 6 to use language-check')