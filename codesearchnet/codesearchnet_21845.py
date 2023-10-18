def status_job(self, fn=None, name=None, timeout=3):
        """Decorator that invokes `add_status_job`.

        ::

            @app.status_job
            def postgresql():
                # query/ping postgres

            @app.status_job(name="Active Directory")
            def active_directory():
                # query active directory

            @app.status_job(timeout=5)
            def paypal():
                # query paypal, timeout after 5 seconds

        """
        if fn is None:
            def decorator(fn):
                self.add_status_job(fn, name, timeout)
            return decorator
        else:
            self.add_status_job(fn, name, timeout)