def render_lights_debug(self, camera_matrix, projection):
        """Render outlines of light volumes"""
        self.ctx.enable(moderngl.BLEND)
        self.ctx.blend_func = moderngl.SRC_ALPHA, moderngl.ONE_MINUS_SRC_ALPHA

        for light in self.point_lights:
            m_mv = matrix44.multiply(light.matrix, camera_matrix)
            light_size = light.radius
            self.debug_shader["m_proj"].write(projection.tobytes())
            self.debug_shader["m_mv"].write(m_mv.astype('f4').tobytes())
            self.debug_shader["size"].value = light_size
            self.unit_cube.render(self.debug_shader, mode=moderngl.LINE_STRIP)

        self.ctx.disable(moderngl.BLEND)