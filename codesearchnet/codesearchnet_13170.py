def get_all_cards(self, timeout: int=None):
        """Get a list of all the cards in the game

        Parameters
        ----------
        timeout: Optional[int] = None
            Custom timeout that overwrites Client.timeout
        """
        url = self.api.CARDS
        return self._get_model(url, timeout=timeout)