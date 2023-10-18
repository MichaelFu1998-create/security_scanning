def x10_command(self, house_code, unit_number, state):
        """Send X10 command to ??? unit.

        @param house_code (A-P) - example='A'
        @param unit_number (1-16)- example=1 (or None to impact entire house code)
        @param state - Mochad command/state, See
                https://sourceforge.net/p/mochad/code/ci/master/tree/README
                examples=OFF, 'OFF', 'ON', ALL_OFF, 'all_units_off', 'xdim 128', etc.

        Examples:
            x10_command('A', '1', ON)
            x10_command('A', '1', OFF)
            x10_command('A', '1', 'ON')
            x10_command('A', '1', 'OFF')
            x10_command('A', None, ON)
            x10_command('A', None, OFF)
            x10_command('A', None, 'all_lights_off')
            x10_command('A', None, 'all_units_off')
            x10_command('A', None, ALL_OFF)
            x10_command('A', None, 'all_lights_on')
            x10_command('A', 1, 'xdim 128')
        """

        house_code = normalize_housecode(house_code)
        if unit_number is not None:
            unit_number = normalize_unitnumber(unit_number)
        # else command is intended for the entire house code, not a single unit number
        # TODO normalize/validate state

        return self._x10_command(house_code, unit_number, state)