def serve_dir(dir_path):
    """
    Generate indexes and run server from the given directory downwards.
    @param {String} dir_path - The directory path (absolute, or relative to CWD)
    @return {None}
    """
    # Create index files, and store the list of their paths for cleanup later
    # This time, force no processing - this gives us a fast first-pass in terms
    # of page generation, but potentially slow serving for large image files
    print('Performing first pass index file generation')
    created_files = _create_index_files(dir_path, True)
    if (PIL_ENABLED):
        # If PIL is enabled, we'd like to process the HTML indexes to include
        # generated thumbnails - this slows down generation so we don't do it
        # first time around, but now we're serving it's good to do in the
        # background
        print('Performing PIL-enchanced optimised index file generation in background')
        background_indexer = BackgroundIndexFileGenerator(dir_path)
        background_indexer.run()
    # Run the server in the current location - this blocks until it's stopped
    _run_server()
    # Clean up the index files created earlier so we don't make a mess of
    # the image directories
    _clean_up(created_files)