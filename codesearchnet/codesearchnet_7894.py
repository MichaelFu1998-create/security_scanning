def _watcher(self):
        """Watch out if we've been disconnected, in that case, kill
        all the jobs.

        """
        while True:
            gevent.sleep(1.0)
            if not self.connected:
                for ns_name, ns in list(six.iteritems(self.active_ns)):
                    ns.recv_disconnect()
                # Killing Socket-level jobs
                gevent.killall(self.jobs)
                break