def get_rarity_info(self, rarity: str):
        """Returns card info from constants

        Parameters
        ---------
        rarity: str
            A rarity name

        Returns None or Constants
        """
        for c in self.constants.rarities:
            if c.name == rarity:
                return c