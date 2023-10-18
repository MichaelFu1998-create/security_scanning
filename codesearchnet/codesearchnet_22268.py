def main(target, label):
    """
    Semver tag triggered deployment helper
    """
    check_environment(target, label)

    click.secho('Fetching tags from the upstream ...')
    handler = TagHandler(git.list_tags())

    print_information(handler, label)

    tag = handler.yield_tag(target, label)
    confirm(tag)