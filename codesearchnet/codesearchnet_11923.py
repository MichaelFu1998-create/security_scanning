def force_stop(self):
        """
        Forcibly terminates all Celery processes.
        """
        r = self.local_renderer
        with self.settings(warn_only=True):
            r.sudo('pkill -9 -f celery')
        r.sudo('rm -f /tmp/celery*.pid')