def draw(self, texture, pos=(0.0, 0.0), scale=(1.0, 1.0)):
        """
        Draw texture using a fullscreen quad.
        By default this will conver the entire screen.

        :param pos: (tuple) offset x, y
        :param scale: (tuple) scale x, y
        """
        if not self.initialized:
            self.init()

        self._texture2d_shader["offset"].value = (pos[0] - 1.0, pos[1] - 1.0)
        self._texture2d_shader["scale"].value = (scale[0], scale[1])
        texture.use(location=0)
        self._texture2d_sampler.use(location=0)
        self._texture2d_shader["texture0"].value = 0
        self._quad.render(self._texture2d_shader)
        self._texture2d_sampler.clear(location=0)