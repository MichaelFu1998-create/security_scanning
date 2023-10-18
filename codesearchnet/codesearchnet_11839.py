def force_stop_and_purge(self):
        """
        Forcibly kills Rabbit and purges all its queues.

        For emergency use when the server becomes unresponsive, even to service stop calls.

        If this also fails to correct the performance issues, the server may have to be completely
        reinstalled.
        """
        r = self.local_renderer
        self.stop()
        with settings(warn_only=True):
            r.sudo('killall rabbitmq-server')
        with settings(warn_only=True):
            r.sudo('killall beam.smp')
        #TODO:explicitly delete all subfolders, star-delete doesn't work
        r.sudo('rm -Rf /var/lib/rabbitmq/mnesia/*')