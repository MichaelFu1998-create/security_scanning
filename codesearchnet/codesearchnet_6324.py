def main(argv):
    """
    Identify the release type and create a new target file with TOML header.

    Requires three arguments.

    """
    source, target, tag = argv
    if "a" in tag:
        bump = "alpha"
    if "b" in tag:
        bump = "beta"
    else:
        bump = find_bump(target, tag)
    filename = "{}.md".format(tag)
    destination = copy(join(source, filename), target)
    build_hugo_md(destination, tag, bump)