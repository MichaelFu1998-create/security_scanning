def handle(self):
        """The main function called to handle a request."""
        while True:
            try:
                line = self.rfile.readline()
                try:
                    # All input data are lines of JSON like the following:
                    #   ["<cmd_name>" "<cmd_arg1>" "<cmd_arg2>" ...]
                    # So I handle this by dispatching to various methods.
                    cmd = json.loads(line)
                except Exception, exc:
                    # Sometimes errors come up. Once again, I can't predict
                    # anything, but can at least tell CouchDB about the error.
                    self.wfile.write(repr(exc) + NEWLINE)
                    continue
                else:
                    # Automagically get the command handler.
                    handler = getattr(self, 'handle_' + cmd[0], None)
                    if not handler:
                        # We are ready to not find commands. It probably won't
                        # happen, but fortune favours the prepared.
                        self.wfile.write(
                            repr(CommandNotFound(cmd[0])) + NEWLINE)
                        continue
                    return_value = handler(*cmd[1:])
                    if not return_value:
                        continue
                    # We write the output back to CouchDB.
                    self.wfile.write(
                        one_lineify(json.dumps(return_value)) + NEWLINE)
            except Exception, exc:
                self.wfile.write(repr(exc) + NEWLINE)
                continue