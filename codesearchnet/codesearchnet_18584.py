def flush(self, line):
        """flush the line to stdout"""
        # TODO -- maybe use echo?
        sys.stdout.write(line)
        sys.stdout.flush()