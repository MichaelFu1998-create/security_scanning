def run(self):
        """
        Attempt to known good or tenuous source.
        """
        with LiveExecution.lock:
            if self.edited_source:
                success, ex = self.run_tenuous()
                if success:
                    return

            self.do_exec(self.known_good, self.ns)