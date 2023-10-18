def close(self):
        """Terminate the controller process and its child processes.

        Args:
              - None
        """
        if self.reuse:
            logger.debug("Ipcontroller not shutting down: reuse enabled")
            return

        if self.mode == "manual":
            logger.debug("Ipcontroller not shutting down: Manual mode")
            return

        try:
            pgid = os.getpgid(self.proc.pid)
            os.killpg(pgid, signal.SIGTERM)
            time.sleep(0.2)
            os.killpg(pgid, signal.SIGKILL)
            try:
                self.proc.wait(timeout=1)
                x = self.proc.returncode
                if x == 0:
                    logger.debug("Controller exited with {0}".format(x))
                else:
                    logger.error("Controller exited with {0}. May require manual cleanup".format(x))
            except subprocess.TimeoutExpired:
                logger.warn("Ipcontroller process:{0} cleanup failed. May require manual cleanup".format(self.proc.pid))

        except Exception as e:
            logger.warn("Failed to kill the ipcontroller process[{0}]: {1}".format(self.proc.pid, e))