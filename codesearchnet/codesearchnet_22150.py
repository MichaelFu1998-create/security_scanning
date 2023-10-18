def maximum_deck_area(self, water_plane_coef=0.88):
        """
        Return the maximum deck area of the ship

        :param water_plane_coef: optional water plane coefficient
        :return: Area of the deck
        """
        AD = self.beam * self.length * water_plane_coef
        return AD