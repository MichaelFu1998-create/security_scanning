def load_source(self):
        """Load the source for the specified file."""
        if self.filename in self.STDIN_NAMES:
            self.filename = "stdin"
            if sys.version_info[0] < 3:
                self.source = sys.stdin.read()
            else:
                self.source = TextIOWrapper(sys.stdin.buffer, errors="ignore").read()
        else:
            # Could be a Python 2.7 StringIO with no context manager, sigh.
            # with tokenize_open(self.filename) as fd:
            #     self.source = fd.read()
            handle = tokenize_open(self.filename)
            self.source = handle.read()
            handle.close()