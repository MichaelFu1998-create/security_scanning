def handle_got_features_event(self, event):
        """Check for roster related features in the stream features received
        and set `server_features` accordingly.
        """
        server_features = set()
        logger.debug("Checking roster-related features")
        if event.features.find(FEATURE_ROSTERVER) is not None:
            logger.debug("  Roster versioning available")
            server_features.add("versioning")
        if event.features.find(FEATURE_APPROVALS) is not None:
            logger.debug("  Subscription pre-approvals available")
            server_features.add("pre-approvals")
        self.server_features = server_features