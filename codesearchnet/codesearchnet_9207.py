def __feed_backend_arthur(self, repo):
        """ Feed Ocean with backend data collected from arthur redis queue"""

        # Always get pending items from arthur for all data sources
        self.__feed_arthur()

        tag = self.backend_tag(repo)

        logger.debug("Arthur items available for %s", self.arthur_items.keys())

        logger.debug("Getting arthur items for %s.", tag)

        if tag in self.arthur_items:
            logger.debug("Found items for %s.", tag)
            while self.arthur_items[tag]:
                yield self.arthur_items[tag].pop()