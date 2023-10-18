def delay(self, positions):
        '''Delay one or more audio channels such that they start at the given
        positions.

        Parameters
        ----------
        positions: list of floats
            List of times (in seconds) to delay each audio channel.
            If fewer positions are given than the number of channels, the
            remaining channels will be unaffected.

        '''
        if not isinstance(positions, list):
            raise ValueError("positions must be a a list of numbers")

        if not all((is_number(p) and p >= 0) for p in positions):
            raise ValueError("positions must be positive nubmers")

        effect_args = ['delay']
        effect_args.extend(['{:f}'.format(p) for p in positions])

        self.effects.extend(effect_args)
        self.effects_log.append('delay')
        return self