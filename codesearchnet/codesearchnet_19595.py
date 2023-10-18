def _create_index_files(root_dir, force_no_processing=False):
    """
    Crawl the root directory downwards, generating an index HTML file in each
    directory on the way down.
    @param {String} root_dir - The top level directory to crawl down from. In
        normal usage, this will be '.'.
    @param {Boolean=False} force_no_processing - If True, do not attempt to
        actually process thumbnails, PIL images or anything. Simply index
        <img> tags with original file src attributes.
    @return {[String]} Full file paths of all created files.
    """
    # Initialise list of created file paths to build up as we make them
    created_files = []
    # Walk the root dir downwards, creating index files as we go
    for here, dirs, files in os.walk(root_dir):
        print('Processing %s' % here)
        # Sort the subdirectories by name
        dirs = sorted(dirs)
        # Get image files - all files in the directory matching IMAGE_FILE_REGEX
        image_files = [f for f in files if re.match(IMAGE_FILE_REGEX, f)]
        # Sort the image files by name
        image_files = sorted(image_files)
        # Create this directory's index file and add its name to the created
        # files list
        created_files.append(
            _create_index_file(
                root_dir, here, image_files, dirs, force_no_processing
            )
        )
    # Return the list of created files
    return created_files