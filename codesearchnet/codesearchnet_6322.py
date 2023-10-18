def build_hugo_md(filename, tag, bump):
    """
    Build the markdown release notes for Hugo.

    Inserts the required TOML header with specific values and adds a break
    for long release notes.

    Parameters
    ----------
    filename : str, path
        The release notes file.
    tag : str
        The tag, following semantic versioning, of the current release.
    bump : {"major", "minor", "patch", "alpha", "beta"}
        The type of release.

    """
    header = [
        '+++\n',
        'date = "{}"\n'.format(date.today().isoformat()),
        'title = "{}"\n'.format(tag),
        'author = "The COBRApy Team"\n',
        'release = "{}"\n'.format(bump),
        '+++\n',
        '\n'
    ]
    with open(filename, "r") as file_h:
        content = insert_break(file_h.readlines())
    header.extend(content)
    with open(filename, "w") as file_h:
        file_h.writelines(header)