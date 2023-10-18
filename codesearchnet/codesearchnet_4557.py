def _hold_block(self, block_id):
        """ Sends hold command to all managers which are in a specific block

        Parameters
        ----------
        block_id : str
             Block identifier of the block to be put on hold
        """

        managers = self.connected_managers

        for manager in managers:
            if manager['block_id'] == block_id:
                logger.debug("[HOLD_BLOCK]: Sending hold to manager:{}".format(manager['manager']))
                self.hold_worker(manager['manager'])