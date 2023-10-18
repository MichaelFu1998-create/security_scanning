def parse_java_version(version_text):
    """Return Java version (major1, major2).

    >>> parse_java_version('''java version "1.6.0_65"
    ... Java(TM) SE Runtime Environment (build 1.6.0_65-b14-462-11M4609)
    ... Java HotSpot(TM) 64-Bit Server VM (build 20.65-b04-462, mixed mode))
    ... ''')
    (1, 6)

    >>> parse_java_version('''
    ... openjdk version "1.8.0_60"
    ... OpenJDK Runtime Environment (build 1.8.0_60-b27)
    ... OpenJDK 64-Bit Server VM (build 25.60-b23, mixed mode))
    ... ''')
    (1, 8)

    """
    match = re.search(JAVA_VERSION_REGEX, version_text)
    if not match:
        raise SystemExit(
            'Could not parse Java version from """{}""".'.format(version_text))

    return (int(match.group('major1')), int(match.group('major2')))