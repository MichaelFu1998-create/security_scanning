def copy_web_file_to_local(file_path, target_path):
    """Copies a file from its location on the web to a designated 
    place on the local machine.

    Args:
        file_path: Complete url of the file to copy, string (e.g. http://fool.com/input.css).

        target_path: Path and name of file on the local machine, string. (e.g. /directory/output.css)

    Returns:
        None.

    """
    response = urllib.request.urlopen(file_path)
    f = open(target_path, 'w')
    f.write(response.read()) 
    f.close()