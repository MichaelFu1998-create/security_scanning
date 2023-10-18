def run(self):
        """Request client connection and start the main loop."""
        if self.args.roster_cache and os.path.exists(self.args.roster_cache):
            logging.info(u"Loading roster from {0!r}"
                                            .format(self.args.roster_cache))
            try:
                self.client.roster_client.load_roster(self.args.roster_cache)
            except (IOError, ValueError), err:
                logging.error(u"Could not load the roster: {0!r}".format(err))
        self.client.connect()
        self.client.run()