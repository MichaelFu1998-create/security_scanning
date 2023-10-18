def run(self):
        """
        The entry point of this script to generate change log
        'ChangelogGeneratorError' Is thrown when one
        of the specified tags was not found in list of tags.
        """
        if not self.options.project or not self.options.user:
            print("Project and/or user missing. "
                  "For help run:\n  pygcgen --help")
            return

        if not self.options.quiet:
            print("Generating changelog...")

        log = None
        try:
            log = self.generator.compound_changelog()
        except ChangelogGeneratorError as err:
            print("\n\033[91m\033[1m{}\x1b[0m".format(err.args[0]))
            exit(1)
        if not log:
            if not self.options.quiet:
                print("Empty changelog generated. {} not written.".format(
                    self.options.output)
                )
            return

        if self.options.no_overwrite:
            out = checkname(self.options.output)
        else:
            out = self.options.output

        with codecs.open(out, "w", "utf-8") as fh:
            fh.write(log)

        if not self.options.quiet:
            print("Done!")
            print("Generated changelog written to {}".format(out))