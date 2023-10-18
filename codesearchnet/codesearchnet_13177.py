def get_card_info(self, card_name: str):
        """Returns card info from constants

        Parameters
        ---------
        card_name: str
            A card name

        Returns None or Constants
        """
        for c in self.constants.cards:
            if c.name == card_name:
                return c