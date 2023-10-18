def _mount_repo(repo, wait_for_server=False):
    """
    This function will create the VM directory where a repo will be mounted, if it
    doesn't exist.  If wait_for_server is set, it will wait up to 10 seconds for
    the nfs server to start, by retrying mounts that fail with 'Connection Refused'.

    If wait_for_server is not set, it will attempt to run the mount command once
    """
    check_call_on_vm('sudo mkdir -p {}'.format(repo.vm_path))
    if wait_for_server:
        for i in range(0,10):
            try:
                _run_mount_command(repo)
                return
            except CalledProcessError as e:
                if 'Connection refused' in e.output:
                    logging.info('Failed to mount repo; waiting for nfsd to restart')
                    time.sleep(1)
                else:
                    logging.info(e.output)
                    raise e
        log_to_client('Failed to mount repo {}'.format(repo.short_name))
        raise RuntimeError('Unable to mount repo with NFS')
    else:
        _run_mount_command(repo)