def speed(self, framerate=None):
        '''Set animation framerate.

        :param framerate: Frames per second to run bot.
        :return: Current framerate of animation.
        '''
        if framerate is not None:
            self._speed = framerate
            self._dynamic = True
        else:
            return self._speed