def parse_repo_slug_from_url(github_url):
    """Get the slug, <owner>/<repo_name>, for a GitHub repository from
    its URL.

    Parameters
    ----------
    github_url : `str`
        URL of a GitHub repository.

    Returns
    -------
    repo_slug : `RepoSlug`
        Repository slug with fields ``full``, ``owner``, and ``repo``.
        See `RepoSlug` for details.

    Raises
    ------
    RuntimeError
        Raised if the URL cannot be parsed.
    """
    match = GITHUB_SLUG_PATTERN.match(github_url)
    if not match:
        message = 'Could not parse GitHub slug from {}'.format(github_url)
        raise RuntimeError(message)

    _full = '/'.join((match.group('org'),
                      match.group('name')))
    return RepoSlug(_full, match.group('org'), match.group('name'))