def extract_files(filename, includes):
    """
    Extract the files to be added based on the includes
    """

    # Load the execution strace log
    lines = open(filename).readlines()

    # Extract only open files - whether for read or write. You often
    # want to capture the json/ini configuration file as well
    files = {}
    lines = [l.strip() for l in lines if 'open(' in l]
    for l in lines:

        # Check both these formats...
        # 20826 open("/usr/lib/locale/locale-archive", O_RDONLY|O_CLOEXEC) = 3
        #[28940] access(b'/etc/ld.so.nohwcap', F_OK)      = -2 (No such file or directory)
        matchedfile = re.search('open\([b]["\'](.+?)["\']', l)
        if matchedfile is None:
            matchedfile = re.search('open\("(.+?)\"', l)

        if matchedfile is None:
            continue

        matchedfile = matchedfile.group(1)

        if os.path.exists(matchedfile) and os.path.isfile(matchedfile):

            #print("Looking at ", matchedfile)

            # Check what action is being performed on these
            action = 'input' if 'O_RDONLY' in l else 'output'

            matchedfile = os.path.relpath(matchedfile, ".")
            #print("Matched file's relative path", matchedfile)

            for i in includes:
                if fnmatch.fnmatch(matchedfile, i):
                    # Exclude python libraries
                    if 'site-packages' in matchedfile:
                        continue
                    if matchedfile not in files:
                        files[matchedfile] = [action]
                    else:
                        if action not in files[matchedfile]:
                            files[matchedfile].append(action)

    # A single file may be opened and closed multiple times

    if len(files) == 0:
        print("No input or output files found that match pattern")
        return []

    print('We captured files that matched the pattern you specified.')
    print('Please select files to keep (press ENTER)')

    # Let the user have the final say on which files must be included.
    filenames = list(files.keys())
    filenames.sort()
    with tempfile.NamedTemporaryFile(suffix=".tmp") as temp:
        temp.write(yaml.dump(filenames, default_flow_style=False).encode('utf-8'))
        temp.flush()
        EDITOR = os.environ.get('EDITOR','/usr/bin/vi')
        subprocess.call("%s %s" %(EDITOR,temp.name), shell=True)
        temp.seek(0)
        data = temp.read()
        selected = yaml.load(data)

    print("You selected", len(selected), "file(s)")
    if len(selected) == 0:
        return []

    # Get the action corresponding to the selected files
    filenames = [f for f in filenames if f in selected]

    # Now we know the list of files. Where should they go?
    print('Please select target locations for the various directories we found')
    print('Please make sure you do not delete any rows or edit the keys.')
    input('(press ENTER)')
    prefixes = {}
    for f in filenames:
        dirname = os.path.dirname(f)
        if dirname == "":
            dirname = "."
        prefixes[dirname] = dirname

    while True:
        with tempfile.NamedTemporaryFile(suffix=".tmp") as temp:
            temp.write(yaml.dump(prefixes, default_flow_style=False).encode('utf-8'))
            temp.flush()
            EDITOR = os.environ.get('EDITOR','/usr/bin/vi')
            subprocess.call("%s %s" %(EDITOR,temp.name), shell=True)
            temp.seek(0)
            data = temp.read()
            try:
                revised = yaml.load(data)
            except Exception as e:
                revised = {}

            #print(list(revised.keys()))
            #print(list(prefixes.keys()))

            if set(list(revised.keys())) == set(list(prefixes.keys())):
                prefixes = revised
                break
            else:
                print("Could not process edited file. Either some rows are missing or entry has YAML syntax errors")
                input("Press ENTER to continue")

    # Add the root directory back
    if "." in prefixes:
        prefixes[""] = prefixes["."]

    result = []
    ts = datetime.now().isoformat()
    for f in filenames:
        relativepath = prefixes[os.path.dirname(f)]
        if relativepath == ".":
            relativepath = os.path.basename(f)
        else:
            relativepath = os.path.join(relativepath, os.path.basename(f))

        result.append(OrderedDict([
            ('relativepath', relativepath),
            ('type', 'run-output'),
            ('actions', files[f]),
            ('mimetypes', mimetypes.guess_type(f)[0]),
            ('content', open(f).read(512)),
            ('sha256', compute_sha256(f)),
            ('ts', ts),
            ('localrelativepath', os.path.relpath(f, ".")),
            ('localfullpath', os.path.abspath(f)),
        ]))

    print(json.dumps(result, indent=4))
    return result