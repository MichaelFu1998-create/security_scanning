def parse_requirements(filename):
    """Parse out a list of requirements from the given requirements
    requirements file.
    """
    reqs = []
    version_spec_in_play = None

    # Iterate over each line in the requirements file.
    for line in open(filename, 'r').read().strip().split('\n'):
        # Sanity check: Is this an empty line?
        # If so, do nothing.
        if not line.strip():
            continue

        # If this is just a plain requirement (not a comment), then
        # add it to the requirements list.
        if not line.startswith('#'):
            reqs.append(line)
            continue

        # "Header" comments take the form of "=== Python {op} {version} ===",
        # and make the requirement only matter for those versions.
        # If this line is a header comment, parse it.
        match = re.search(r'^# === [Pp]ython (?P<op>[<>=]{1,2}) '
                          r'(?P<major>[\d])\.(?P<minor>[\d]+) ===[\s]*$', line)
        if match:
            version_spec_in_play = match.groupdict()
            for key in ('major', 'minor'):
                version_spec_in_play[key] = int(version_spec_in_play[key])
            continue

        # If this is a comment that otherwise looks like a package, then it
        # should be a package applying only to the current version spec.
        #
        # We can identify something that looks like a package by a lack
        # of any spaces.
        if ' ' not in line[1:].strip() and version_spec_in_play:
            package = line[1:].strip()

            # Sanity check: Is our version of Python one of the ones currently
            # in play?
            op = version_spec_in_play['op']
            vspec = (version_spec_in_play['major'],
                     version_spec_in_play['minor'])
            if '=' in op and sys.version_info[0:2] == vspec:
                reqs.append(package)
            elif '>' in op and sys.version_info[0:2] > vspec:
                reqs.append(package)
            elif '<' in op and sys.version_info[0:2] < vspec:
                reqs.append(package)

    # Okay, we should have an entire list of requirements now.
    return reqs