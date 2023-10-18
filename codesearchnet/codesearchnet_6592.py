def sendToTradepile(self, item_id, safe=True):
        """Send to tradepile (alias for __sendToPile__).

        :params item_id: Item id.
        :params safe: (optional) False to disable tradepile free space check.
        """
        if safe and len(
                self.tradepile()) >= self.tradepile_size:  # TODO?: optimization (don't parse items in tradepile)
            return False
        return self.__sendToPile__('trade', item_id=item_id)