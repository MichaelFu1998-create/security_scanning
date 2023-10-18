def scale_in(self, blocks):
        """Scale in the number of active blocks by the specified number.

        """
        status = dict(zip(self.engines, self.provider.status(self.engines)))

        # This works for blocks=0
        to_kill = [engine for engine in status if status[engine] == "RUNNING"][:blocks]

        if self.provider:
            r = self.provider.cancel(to_kill)
        else:
            logger.error("No execution provider available")
            r = None

        return r