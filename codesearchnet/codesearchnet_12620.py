def quit(self):
        """
        Quit the player, blocking until the process has died
        """
        if self._process is None:
            logger.debug('Quit was called after self._process had already been released')
            return
        try:
            logger.debug('Quitting OMXPlayer')
            process_group_id = os.getpgid(self._process.pid)
            os.killpg(process_group_id, signal.SIGTERM)
            logger.debug('SIGTERM Sent to pid: %s' % process_group_id)
            self._process_monitor.join()
        except OSError:
            logger.error('Could not find the process to kill')

        self._process = None