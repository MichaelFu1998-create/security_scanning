def prop_power(self, propulsion_eff=0.7, sea_margin=0.2):
        """
        Total propulsion power of the ship.

        :param propulsion_eff: Shaft efficiency of the ship
        :param sea_margin: Sea margin take account of interaction between ship and the sea, e.g. wave
        :return: Watts shaft propulsion power of the ship
        """
        PP = (1 + sea_margin) * self.resistance() * self.speed/propulsion_eff
        return PP