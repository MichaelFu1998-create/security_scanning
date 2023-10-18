def cardInfo(self, resource_id):
        """Return card info.

        :params resource_id: Resource id.
        """
        # TODO: add referer to headers (futweb)
        base_id = baseId(resource_id)
        if base_id in self.players:
            return self.players[base_id]
        else:  # not a player?
            url = '{0}{1}.json'.format(card_info_url, base_id)
            return requests.get(url, timeout=self.timeout).json()