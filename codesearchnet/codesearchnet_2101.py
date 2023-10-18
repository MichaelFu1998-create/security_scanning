def _int_to_pos(self, flat_position):
        """Returns x, y from flat_position integer.

        Args:
            flat_position: flattened position integer

        Returns: x, y

        """
        return flat_position % self.env.action_space.screen_shape[0],\
            flat_position % self.env.action_space.screen_shape[1]