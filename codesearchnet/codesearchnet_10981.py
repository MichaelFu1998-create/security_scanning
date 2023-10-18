def draw_buffers(self, near, far):
        """
        Draw framebuffers for debug purposes.
        We need to supply near and far plane so the depth buffer can be linearized when visualizing.

        :param near: Projection near value
        :param far: Projection far value
        """
        self.ctx.disable(moderngl.DEPTH_TEST)

        helper.draw(self.gbuffer.color_attachments[0], pos=(0.0, 0.0), scale=(0.25, 0.25))
        helper.draw(self.gbuffer.color_attachments[1], pos=(0.5, 0.0), scale=(0.25, 0.25))
        helper.draw_depth(self.gbuffer.depth_attachment, near, far, pos=(1.0, 0.0), scale=(0.25, 0.25))
        helper.draw(self.lightbuffer.color_attachments[0], pos=(1.5, 0.0), scale=(0.25, 0.25))