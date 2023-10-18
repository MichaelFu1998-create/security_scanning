def update_backend(use_pypi=False, index='dev', build=True, user=None, version=None):
    """
    Install the backend from the given devpi index at the given version on the target host and restart the service.

    If version is None, it defaults to the latest version

    Optionally, build and upload the application first from local sources. This requires a
    full backend development environment on the machine running this command (pyramid etc.)
    """
    get_vars()
    if value_asbool(build):
        upload_backend(index=index, user=user)
    with fab.cd('{apphome}'.format(**AV)):
        if value_asbool(use_pypi):
            command = 'bin/pip install --upgrade briefkasten'
        else:
            command = 'bin/pip install --upgrade --pre -i {ploy_default_publish_devpi}/briefkasten/{index}/+simple/ briefkasten'.format(
                index=index,
                user=user,
                **AV)
        if version:
            command = '%s==%s' % (command, version)
        fab.sudo(command)

    briefkasten_ctl('restart')