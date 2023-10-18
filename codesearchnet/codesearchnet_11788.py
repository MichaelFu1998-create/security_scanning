def install_config(local_path=None, remote_path=None, render=True, extra=None, formatter=None):
    """
    Returns a template to a remote file.
    If no filename given, a temporary filename will be generated and returned.
    """
    local_path = find_template(local_path)
    if render:
        extra = extra or {}
        local_path = render_to_file(template=local_path, extra=extra, formatter=formatter)
    put_or_dryrun(local_path=local_path, remote_path=remote_path, use_sudo=True)