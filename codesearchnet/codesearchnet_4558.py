def scale_out(self, blocks=1):
        """Scales out the number of blocks by "blocks"

        Raises:
             NotImplementedError
        """
        r = []
        for i in range(blocks):
            if self.provider:
                external_block_id = str(len(self.blocks))
                launch_cmd = self.launch_cmd.format(block_id=external_block_id)
                internal_block = self.provider.submit(launch_cmd, 1, 1)
                logger.debug("Launched block {}->{}".format(external_block_id, internal_block))
                if not internal_block:
                    raise(ScalingFailed(self.provider.label,
                                        "Attempts to provision nodes via provider has failed"))
                r.extend([external_block_id])
                self.blocks[external_block_id] = internal_block
            else:
                logger.error("No execution provider available")
                r = None
        return r