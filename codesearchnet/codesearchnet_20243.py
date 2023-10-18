def auto_init(autofile, force_init=False):
    """
    Initialize a repo-specific configuration file to execute dgit

    Parameters
    ----------

    autofile: Repo-specific configuration file (dgit.json)
    force_init: Flag to force to re-initialization of the configuration file

    """

    if os.path.exists(autofile) and not force_init:
        try:
            autooptions = json.loads(open(autofile).read())
            return autooptions
        except:
            print("Error in dgit.json configuration file")
            traceback.print_exc()
            raise Exception("Invalid configuration file")

    config = get_config()
    pluginmgr = plugins_get_mgr()

    print("Repo configuration file missing or corrupted. Creating one")
    print("Let us know a few details about your data repository")

    # Get the username
    username = getpass.getuser()
    revised = input("Please specify username [{}]".format(username))
    if revised not in ["", None]:
        username = revised

    # Get the reponame
    thisdir = os.path.abspath(os.getcwd())
    reponame = os.path.basename(thisdir)
    revised = input("Please specify repo name [{}]".format(reponame))
    if revised not in ["", None]:
        reponame = revised

    # Get the default backend URL
    keys = pluginmgr.search('backend')
    keys = keys['backend']
    keys = [k for k in keys if k[0] != "local"]
    remoteurl = ""
    backend = None
    if len(keys) > 0:
        backend = pluginmgr.get_by_key('backend', keys[0])
        candidate = backend.url(username, reponame)
        revised = input("Please specify remote URL [{}]".format(candidate))
        if revised in ["", None]:
            remoteurl = candidate
        else:
            remoteurl = revised

    # Get title...
    title = ""
    while title == "":
        title = input("One line summary of your repo:")
        if title == "":
            print("The repo requires a one line summary")
        else:
            break

    # Get description
    description = ""
    while description == "":
        description = input("Detailed description:")
        if description == "":
            print("The repo requires some text as well")
        else:
            break

    autooptions = OrderedDict([
        ("username", username),
        ("reponame", reponame),
        ("remoteurl", remoteurl),
        ("title", title),
        ("description", description),
        ("working-directory", "."),
        ('track' ,OrderedDict([
            ('includes', ['*.csv', '*.tsv', '*.txt','*.json', '*.xls', '*.xlsx', "*.sql", "*.hql"]),
            ('excludes', ['.git', '.svn', os.path.basename(autofile)]),
        ])),
        ('auto-push', False),
        ('pipeline' ,OrderedDict([])),
        ('import' ,OrderedDict([
            ('directory-mapping' ,OrderedDict([
                ('.', '')
            ]))
        ])),
        ('dependencies' ,OrderedDict([]))
    ])

    # Gather options from each of the enabled plugins
    for p in ['validator', 'transformer']:
        keys = pluginmgr.search(p)
        keys = keys[p]
        options = OrderedDict()
        for k in keys:
            if k.name in options:
                continue
            mgr = pluginmgr.get_by_key(p, k)
            options[k.name] = mgr.autooptions()
        autooptions[p] = options

    keys = pluginmgr.search('metadata')
    keys = keys['metadata']
    if len(keys) > 0:

        # => Select domains that be included.
        servers = []
        for k in keys:
            server = pluginmgr.get_by_key('metadata', k)
            server = server.url.split("/")[2]
            servers.append(server)

        # Specify what should be included. Some of these should go ino
        # the metadata modules

        autooptions.update(OrderedDict([
            ('metadata-management', OrderedDict([
                ('servers', servers),
                ('include-code-history', find_executable_files()),
                ('include-preview', OrderedDict([
                    ('length', 512),
                    ('files', ['*.txt', '*.csv', '*.tsv'])
                    ])),
                ('include-data-history', True),
                ('include-action-history', True),
                ('include-validation', True),
                ('include-dependencies', True),
                ('include-schema', True),
                ('include-tab-diffs', True),
                ('include-platform', True),
            ]))]))

    with open(autofile, 'w') as fd:
        fd.write(json.dumps(autooptions, indent=4))

    print("")
    print("Updated dataset specific config file: {}".format(autofile))
    print("Please edit it and rerun dgit auto.")
    print("Tip: Consider committing dgit.json to the code repository.")

    #if platform.system() == "Linux":
    #    subprocess.call(["xdg-open", autofile])

    sys.exit()