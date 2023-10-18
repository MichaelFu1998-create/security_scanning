def restart(self):
        """
        Supervisor can take a very long time to start and stop,
        so wait for it.
        """
        n = 60
        sleep_n = int(self.env.max_restart_wait_minutes/10.*60)
        for _ in xrange(n):
            self.stop()
            if self.dryrun or not self.is_running():
                break
            print('Waiting for supervisor to stop (%i of %i)...' % (_, n))
            time.sleep(sleep_n)
        self.start()
        for _ in xrange(n):
            if self.dryrun or self.is_running():
                return
            print('Waiting for supervisor to start (%i of %i)...' % (_, n))
            time.sleep(sleep_n)
        raise Exception('Failed to restart service %s!' % self.name)