def _save_private_file(filename, json_contents):
    """Saves a file with read-write permissions on for the owner.

    Args:
        filename: String. Absolute path to file.
        json_contents: JSON serializable object to be saved.
    """
    temp_filename = tempfile.mktemp()
    file_desc = os.open(temp_filename, os.O_WRONLY | os.O_CREAT, 0o600)
    with os.fdopen(file_desc, 'w') as file_handle:
        json.dump(json_contents, file_handle, sort_keys=True,
                  indent=2, separators=(',', ': '))
    shutil.move(temp_filename, filename)