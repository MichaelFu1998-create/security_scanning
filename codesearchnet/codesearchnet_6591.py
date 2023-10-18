def tradepileDelete(self, trade_id):  # item_id instead of trade_id?
        """Remove card from tradepile.

        :params trade_id: Trade id.
        """
        method = 'DELETE'
        url = 'trade/%s' % trade_id

        self.__request__(method, url)  # returns nothing
        # TODO: validate status code
        return True