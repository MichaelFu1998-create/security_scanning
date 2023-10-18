def bootstrap_datapackage(repo, force=False,
                          options=None, noinput=False):
    """
    Create the datapackage file..
    """

    print("Bootstrapping datapackage")

    # get the directory
    tsprefix = datetime.now().date().isoformat()

    # Initial data package json
    package = OrderedDict([
        ('title', ''),
        ('description', ''),
        ('username', repo.username),
        ('reponame', repo.reponame),
        ('name', str(repo)),
        ('title', ""),
        ('description', ""),
        ('keywords', []),
        ('resources', []),
        ('creator', getpass.getuser()),
        ('createdat', datetime.now().isoformat()),
        ('remote-url', repo.remoteurl)
    ])

    if options is not None:
        package['title'] = options['title']
        package['description'] = options['description']
    else:
        if noinput:
            raise IncompleteParameters("Option field with title and description")

        for var in ['title', 'description']:
            value = ''
            while value in ['',None]:
                value = input('Your Repo ' + var.title() + ": ")
                if len(value) == 0:
                    print("{} cannot be empty. Please re-enter.".format(var.title()))

            package[var] = value


    # Now store the package...
    (handle, filename) = tempfile.mkstemp()
    with open(filename, 'w') as fd:
        fd.write(json.dumps(package, indent=4))

    repo.package = package

    return filename