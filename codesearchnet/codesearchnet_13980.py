def run_tenuous(self):
        """
        Run edited source, if no exceptions occur then it
        graduates to known good.
        """
        with LiveExecution.lock:
            ns_snapshot = copy.copy(self.ns)
            try:
                source = self.edited_source
                self.edited_source = None
                self.do_exec(source, ns_snapshot)
                self.known_good = source
                self.call_good_cb()
                return True, None
            except Exception as ex:
                tb = traceback.format_exc()
                self.call_bad_cb(tb)
                self.ns.clear()
                self.ns.update(ns_snapshot)
                return False, ex