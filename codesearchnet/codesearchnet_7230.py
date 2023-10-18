def _get_position(self, position, prev=False):
        """Return the next/previous position or raise IndexError."""
        if position == self.POSITION_LOADING:
            if prev:
                raise IndexError('Reached last position')
            else:
                return self._conversation.events[0].id_
        else:
            ev = self._conversation.next_event(position, prev=prev)
            if ev is None:
                if prev:
                    return self.POSITION_LOADING
                else:
                    raise IndexError('Reached first position')
            else:
                return ev.id_