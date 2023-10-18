def get_files_to_commit(autooptions):
    """
    Look through the local directory to pick up files to check
    """
    workingdir = autooptions['working-directory']
    includes = autooptions['track']['includes']
    excludes = autooptions['track']['excludes']

    # transform glob patterns to regular expressions
    # print("Includes ", includes) 
    includes = r'|'.join([fnmatch.translate(x) for x in includes])
    excludes = r'|'.join([fnmatch.translate(x) for x in excludes]) or r'$.'

    matched_files = []
    for root, dirs, files in os.walk(workingdir):

        # print("Looking at ", files)

        # exclude dirs
        # dirs[:] = [os.path.join(root, d) for d in dirs]
        dirs[:] = [d for d in dirs if not re.match(excludes, d)]

        # exclude/include files
        files = [f for f in files if not re.match(excludes, f)]
        #print("Files after excludes", files)
        #print(includes) 
        files = [f for f in files if re.match(includes, f)]
        #print("Files after includes", files) 
        files = [os.path.join(root, f) for f in files]

        matched_files.extend(files)

    return matched_files