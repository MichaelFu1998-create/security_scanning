def run_executable(repo, args, includes):
    """
    Run the executable and capture the input and output...
    """

    # Get platform information
    mgr = plugins_get_mgr()
    repomgr = mgr.get(what='instrumentation', name='platform')
    platform_metadata = repomgr.get_metadata()

    print("Obtaining Commit Information")
    (executable, commiturl) = \
            find_executable_commitpath(repo, args)

    # Create a local directory
    tmpdir = tempfile.mkdtemp()

    # Construct the strace command
    print("Running the command")
    strace_filename = os.path.join(tmpdir,'strace.out.txt')
    cmd = ["strace.py", "-f", "-o", strace_filename,
           "-s", "1024", "-q", "--"] + args

    # Run the command
    p = subprocess.Popen(cmd,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    out, err = p.communicate()

    # Capture the stdout/stderr
    stdout = os.path.join(tmpdir, 'stdout.log.txt')
    with open(stdout, 'w') as fd:
        fd.write(out.decode('utf-8'))

    stderr = os.path.join(tmpdir, 'stderr.log.txt')
    with open(stderr, 'w') as fd:
        fd.write(err.decode('utf-8'))


    # Check the strace output
    files = extract_files(strace_filename, includes)


    # Now insert the execution metadata
    execution_metadata = {
        'likelyexecutable': executable,
        'commitpath': commiturl,
        'args': args,
    }
    execution_metadata.update(platform_metadata)

    for i in range(len(files)):
        files[i]['execution_metadata'] = execution_metadata

    return files