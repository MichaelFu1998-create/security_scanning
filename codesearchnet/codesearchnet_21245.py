def modify_data(data):
    """
        Creates a tempfile and starts the given editor, returns the data afterwards.
    """
    with tempfile.NamedTemporaryFile('w') as f:
        for entry in data:
            f.write(json.dumps(entry.to_dict(
                include_meta=True),
                default=datetime_handler))
            f.write('\n')
        f.flush()
        print_success("Starting editor")
        subprocess.call(['nano', '-', f.name])
        with open(f.name, 'r') as f:
            return f.readlines()