def set_permissions(self):
        """
        Sets ownership and permissions for Celery-related files.
        """
        r = self.local_renderer
        for path in r.env.paths_owned:
            r.env.path_owned = path
            r.sudo('chown {celery_daemon_user}:{celery_daemon_user} {celery_path_owned}')