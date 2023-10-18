def _spawn_receiver_loop(self):
        """Spawns the reader loop.  This is called internall by
        socketio_manage().
        """
        job = gevent.spawn(self._receiver_loop)
        self.jobs.append(job)
        return job