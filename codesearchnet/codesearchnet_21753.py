def get_content_commit_date(extensions, acceptance_callback=None,
                            root_dir='.'):
    """Get the datetime for the most recent commit to a project that
    affected certain types of content.

    Parameters
    ----------
    extensions : sequence of 'str'
        Extensions of files to consider in getting the most recent commit
        date. For example, ``('rst', 'svg', 'png')`` are content extensions
        for a Sphinx project. **Extension comparision is case sensitive.** add
        uppercase variants to match uppercase extensions.
    acceptance_callback : callable
        Callable function whose sole argument is a file path, and returns
        `True` or `False` depending on whether the file's commit date should
        be considered or not. This callback is only run on files that are
        included by ``extensions``. Thus this callback is a way to exclude
        specific files that would otherwise be included by their extension.
    root_dir : 'str`, optional
        Only content contained within this root directory is considered.
        This directory must be, or be contained by, a Git repository. This is
        the current working directory by default.

    Returns
    -------
    commit_date : `datetime.datetime`
        Datetime of the most recent content commit.

    Raises
    ------
    RuntimeError
        Raised if no content files are found.
    """
    logger = logging.getLogger(__name__)

    def _null_callback(_):
        return True

    if acceptance_callback is None:
        acceptance_callback = _null_callback

    # Cache the repo object for each query
    root_dir = os.path.abspath(root_dir)
    repo = git.repo.base.Repo(path=root_dir, search_parent_directories=True)

    # Iterate over all files with all file extensions, looking for the
    # newest commit datetime.
    newest_datetime = None
    iters = [_iter_filepaths_with_extension(ext, root_dir=root_dir)
             for ext in extensions]
    for content_path in itertools.chain(*iters):
        content_path = os.path.abspath(os.path.join(root_dir, content_path))

        if acceptance_callback(content_path):
            logger.debug('Found content path %r', content_path)
            try:
                commit_datetime = read_git_commit_timestamp_for_file(
                    content_path, repo=repo)
                logger.debug('Commit timestamp of %r is %s',
                             content_path, commit_datetime)
            except IOError:
                logger.warning(
                    'Count not get commit for %r, skipping',
                    content_path)
                continue

            if not newest_datetime or commit_datetime > newest_datetime:
                # Seed initial newest_datetime
                # or set a newer newest_datetime
                newest_datetime = commit_datetime
                logger.debug('Newest commit timestamp is %s', newest_datetime)

        logger.debug('Final commit timestamp is %s', newest_datetime)

    if newest_datetime is None:
        raise RuntimeError('No content files found in {}'.format(root_dir))

    return newest_datetime