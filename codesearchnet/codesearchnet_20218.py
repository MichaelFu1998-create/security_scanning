def shellcmd(repo, args):
    """
    Run a shell command within the repo's context

    Parameters
    ----------

    repo: Repository object
    args: Shell command
    """
    with cd(repo.rootdir):
        result = run(args)
        return result