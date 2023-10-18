def run_context(self):
        """
        Context in which the user can run the source in a custom manner.

        If no exceptions occur then the source will move from 'tenuous'
        to 'known good'.

        >>> with run_context() as (known_good, source, ns):
        >>> ...  exec source in ns
        >>> ...  ns['draw']()

        """
        with LiveExecution.lock:
            if self.edited_source is None:
                yield True, self.known_good, self.ns
                return

            ns_snapshot = copy.copy(self.ns)
            try:
                yield False, self.edited_source, self.ns
                self.known_good = self.edited_source
                self.edited_source = None
                self.call_good_cb()
                return
            except Exception as ex:
                tb = traceback.format_exc()
                self.call_bad_cb(tb)
                self.edited_source = None
                self.ns.clear()
                self.ns.update(ns_snapshot)