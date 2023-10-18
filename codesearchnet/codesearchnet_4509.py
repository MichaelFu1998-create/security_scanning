def scale_out(self, blocks=1):
        """Scales out the number of active workers by 1.

        This method is notImplemented for threads and will raise the error if called.

        Parameters:
            blocks : int
               Number of blocks to be provisioned.
        """
        r = []
        for i in range(blocks):
            if self.provider:
                block = self.provider.submit(self.launch_cmd, 1, self.workers_per_node)
                logger.debug("Launched block {}:{}".format(i, block))
                if not block:
                    raise(ScalingFailed(self.provider.label,
                                        "Attempts to provision nodes via provider has failed"))
                self.engines.extend([block])
                r.extend([block])
        else:
            logger.error("No execution provider available")
            r = None

        return r