def main():
    """
    Main method.

    This method holds what you want to execute when
    the script is run on command line.
    """
    args = get_arguments()
    setup_logging(args)

    version_path = os.path.abspath(os.path.join(
        os.path.dirname(__file__),
        '..',
        '..',
        '.VERSION'
    ))

    try:
        version_text = open(version_path).read().strip()
    except Exception:
        print('Could not open or read the .VERSION file')
        sys.exit(1)

    try:
        semver.parse(version_text)
    except ValueError:
        print(('The .VERSION file contains an invalid '
               'version: "{}"').format(version_text))
        sys.exit(1)

    new_version = version_text
    if args.version:
        try:
            if semver.parse(args.version):
                new_version = args.version
        except Exception:
            print('Could not parse "{}" as a version'.format(args.version))
            sys.exit(1)
    elif args.bump_major:
        new_version = semver.bump_major(version_text)
    elif args.bump_minor:
        new_version = semver.bump_minor(version_text)
    elif args.bump_patch:
        new_version = semver.bump_patch(version_text)

    try:
        with open(version_path, 'w') as version_file:
            version_file.write(new_version)
    except Exception:
        print('Could not write the .VERSION file')
        sys.exit(1)
    print(new_version)