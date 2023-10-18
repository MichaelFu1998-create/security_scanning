def _get_build_path(app_spec):
    """ Given a spec for an app, returns the value of the `build` field for docker-compose.
    If the path is relative, it is expanded and added to the path of the app's repo. """
    if os.path.isabs(app_spec['build']):
        return app_spec['build']
    return os.path.join(Repo(app_spec['repo']).local_path, app_spec['build'])