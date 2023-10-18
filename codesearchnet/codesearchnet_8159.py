def _on_index(self, old_index):
        """
        Override this method to get called right after ``self.index`` is set.

        :param int old_index: the previous index, before it was changed.
        """
        if self.animation:
            log.debug('%s: %s',
                      self.__class__.__name__, self.current_animation.title)
            self.frames = self.animation.generate_frames(False)