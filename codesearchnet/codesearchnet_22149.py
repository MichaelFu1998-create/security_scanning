def resistance(self):
        """
        Return resistance of the vehicle.

        :return: newton the resistance of the ship
        """
        self.total_resistance_coef = frictional_resistance_coef(self.length, self.speed) + \
                                residual_resistance_coef(self.slenderness_coefficient,
                                                         self.prismatic_coefficient,
                                                         froude_number(self.speed, self.length))
        RT = 1 / 2 * self.total_resistance_coef * 1025 * self.surface_area * self.speed ** 2
        return RT