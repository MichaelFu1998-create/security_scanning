def make_raw_content_url(repo_slug, git_ref, file_path):
    """Make a raw content (raw.githubusercontent.com) URL to a file.

    Parameters
    ----------
    repo_slug : `str` or `RepoSlug`
        The repository slug, formatted as either a `str` (``'owner/name'``)
        or a `RepoSlug` object (created by `parse_repo_slug_from_url`).
    git_ref : `str`
        The git ref: a branch name, commit hash, or tag name.
    file_path : `str`
        The POSIX path of the file in the repository tree.
    """
    if isinstance(repo_slug, RepoSlug):
        slug_str = repo_slug.full
    else:
        slug_str = repo_slug

    if file_path.startswith('/'):
        file_path = file_path.lstrip('/')

    template = 'https://raw.githubusercontent.com/{slug}/{git_ref}/{path}'
    return template.format(
        slug=slug_str,
        git_ref=git_ref,
        path=file_path)