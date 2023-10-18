def read_git_commit_timestamp_for_file(filepath, repo_path=None, repo=None):
    """Obtain the timestamp for the most recent commit to a given file in a
    Git repository.

    Parameters
    ----------
    filepath : `str`
        Absolute or repository-relative path for a file.
    repo_path : `str`, optional
        Path to the Git repository. Leave as `None` to use the current working
        directory or if a ``repo`` argument is provided.
    repo : `git.Repo`, optional
        A `git.Repo` instance.

    Returns
    -------
    commit_timestamp : `datetime.datetime`
        The datetime of the most recent commit to the given file.

    Raises
    ------
    IOError
        Raised if the ``filepath`` does not exist in the Git repository.
    """
    logger = logging.getLogger(__name__)

    if repo is None:
        repo = git.repo.base.Repo(path=repo_path,
                                  search_parent_directories=True)
    repo_path = repo.working_tree_dir

    head_commit = repo.head.commit

    # filepath relative to the repo path
    logger.debug('Using Git repo at %r', repo_path)
    filepath = os.path.relpath(
        os.path.abspath(filepath),
        start=repo_path)
    logger.debug('Repo-relative filepath is %r', filepath)

    # Most recent commit datetime of the given file.
    # Don't use head_commit.iter_parents because then it skips the
    # commit of a file that's added but never modified.
    for commit in head_commit.iter_items(repo,
                                         head_commit,
                                         [filepath],
                                         skip=0):
        return commit.committed_datetime

    # Only get here if git could not find the file path in the history
    raise IOError('File {} not found'.format(filepath))