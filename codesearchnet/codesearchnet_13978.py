def load_edited_source(self, source, good_cb=None, bad_cb=None, filename=None):
        """
        Load changed code into the execution environment.

        Until the code is executed correctly, it will be
        in the 'tenuous' state.
        """
        with LiveExecution.lock:
            self.good_cb = good_cb
            self.bad_cb = bad_cb
            try:
                # text compile
                compile(source + '\n\n', filename or self.filename, "exec")
                self.edited_source = source
            except Exception as e:
                if bad_cb:
                    self.edited_source = None
                    tb = traceback.format_exc()
                    self.call_bad_cb(tb)
                return
            if filename is not None:
                self.filename = filename