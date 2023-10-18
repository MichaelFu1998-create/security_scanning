def _build_metadata(): # pylint: disable=too-many-locals, too-many-branches
    "Return project's metadata as a dict."
    # Handle metadata in package source
    expected_keys = ('url', 'version', 'license', 'author', 'author_email', 'long_description', 'keywords')
    metadata = {}
    with io.open(srcfile('src', package_name, '__init__.py'), encoding='utf-8') as handle:
        pkg_init = handle.read()
        # Get default long description from docstring
        metadata['long_description'] = re.search(r'^"""(.+?)^"""$', pkg_init, re.DOTALL|re.MULTILINE).group(1)
        for line in pkg_init.splitlines():
            match = re.match(r"""^__({0})__ += (?P<q>['"])(.+?)(?P=q)$""".format('|'.join(expected_keys)), line)
            if match:
                metadata[match.group(1)] = match.group(3)

    if not all(i in metadata for i in expected_keys):
        raise RuntimeError("Missing or bad metadata in '{0}' package: {1}"
                           .format(name, ', '.join(sorted(set(expected_keys) - set(metadata.keys()))),))

    text = metadata['long_description'].strip()
    if text:
        metadata['description'], text = text.split('.', 1)
        metadata['description'] = ' '.join(metadata['description'].split()).strip() + '.' # normalize whitespace
        metadata['long_description'] = textwrap.dedent(text).strip()
    metadata['keywords'] = metadata['keywords'].replace(',', ' ').strip().split()

    # Load requirements files
    requirements_files = dict(
        install = 'requirements.txt',
        setup = 'setup-requirements.txt',
        test = 'test-requirements.txt',
    )
    requires = {}
    for key, filename in requirements_files.items():
        requires[key] = []
        if os.path.exists(srcfile(filename)):
            with io.open(srcfile(filename), encoding='utf-8') as handle:
                for line in handle:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        if any(line.startswith(i) for i in ('-e', 'http://', 'https://')):
                            line = line.split('#egg=')[1]
                        requires[key].append(line)
    if not any('pytest' == re.split('[\t ,<=>]', i.lower())[0] for i in requires['test']):
        requires['test'].append('pytest') # add missing requirement

    # CLI entry points
    console_scripts = []
    for path, dirs, files in os.walk(srcfile('src', package_name)):
        dirs = [i for i in dirs if not i.startswith('.')]
        if '__main__.py' in files:
            path = path[len(srcfile('src') + os.sep):]
            appname = path.split(os.sep)[-1]
            with io.open(srcfile('src', path, '__main__.py'), encoding='utf-8') as handle:
                for line in handle.readlines():
                    match = re.match(r"""^__app_name__ += (?P<q>['"])(.+?)(?P=q)$""", line)
                    if match:
                        appname = match.group(2)
            console_scripts.append('{0} = {1}.__main__:cli'.format(appname, path.replace(os.sep, '.')))

    # Add some common files to EGG-INFO
    candidate_files = [
        'LICENSE', 'NOTICE',
        'README', 'README.md', 'README.rst', 'README.txt',
        'CHANGES', 'CHANGELOG', 'debian/changelog',
    ]
    data_files = defaultdict(list)
    for filename in candidate_files:
        if os.path.exists(srcfile(filename)):
            data_files['EGG-INFO'].append(filename)

    # Complete project metadata
    classifiers = []
    for classifiers_txt in ('classifiers.txt', 'project.d/classifiers.txt'):
        classifiers_txt = srcfile(classifiers_txt)
        if os.path.exists(classifiers_txt):
            with io.open(classifiers_txt, encoding='utf-8') as handle:
                classifiers = [i.strip() for i in handle if i.strip() and not i.startswith('#')]
            break
    entry_points.setdefault('console_scripts', []).extend(console_scripts)

    metadata.update(dict(
        name = name,
        package_dir = {'': 'src'},
        packages = find_packages(srcfile('src'), exclude=['tests']),
        data_files = data_files.items(),
        zip_safe = False,
        include_package_data = True,
        install_requires = requires['install'],
        setup_requires = requires['setup'],
        tests_require =  requires['test'],
        classifiers = classifiers,
        cmdclass = dict(
            test = PyTest,
        ),
        entry_points = entry_points,
    ))
    return metadata