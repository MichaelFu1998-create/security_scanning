def report(self, linenumber, filename, severity, message, rulename, char):
        """Report a rule violation"""

        if self._print_filename is not None:
            # we print the filename only once. self._print_filename
            # will get reset each time a new file is processed.
            print("+ " + self._print_filename)
            self._print_filename = None

        if severity in (WARNING, ERROR):
            self.counts[severity] += 1
        else:
            self.counts["other"] += 1

        print(self.args.format.format(linenumber=linenumber, filename=filename,
                                      severity=severity, message=message.encode('utf-8'),
                                      rulename=rulename, char=char))