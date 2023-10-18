def draw_depth(self, texture, near, far, pos=(0.0, 0.0), scale=(1.0, 1.0)):
        """
        Draw depth buffer linearized.
        By default this will draw the texture as a full screen quad.
        A sampler will be used to ensure the right conditions to draw the depth buffer.

        :param near: Near plane in projection
        :param far: Far plane in projection
        :param pos: (tuple) offset x, y
        :param scale: (tuple) scale x, y
        """
        if not self.initialized:
            self.init()

        self._depth_shader["offset"].value = (pos[0] - 1.0, pos[1] - 1.0)
        self._depth_shader["scale"].value = (scale[0], scale[1])
        self._depth_shader["near"].value = near
        self._depth_shader["far"].value = far
        self._depth_sampler.use(location=0)
        texture.use(location=0)
        self._depth_shader["texture0"].value = 0
        self._quad.render(self._depth_shader)
        self._depth_sampler.clear(location=0)