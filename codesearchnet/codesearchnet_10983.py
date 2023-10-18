def render_lights(self, camera_matrix, projection):
        """Render light volumes"""
        # Draw light volumes from the inside
        self.ctx.front_face = 'cw'
        self.ctx.blend_func = moderngl.ONE, moderngl.ONE

        helper._depth_sampler.use(location=1)
        with self.lightbuffer_scope:
            for light in self.point_lights:
                # Calc light properties
                light_size = light.radius
                m_light = matrix44.multiply(light.matrix, camera_matrix)
                # Draw the light volume
                self.point_light_shader["m_proj"].write(projection.tobytes())
                self.point_light_shader["m_light"].write(m_light.astype('f4').tobytes())
                self.gbuffer.color_attachments[1].use(location=0)
                self.point_light_shader["g_normal"].value = 0
                self.gbuffer.depth_attachment.use(location=1)
                self.point_light_shader["g_depth"].value = 1
                self.point_light_shader["screensize"].value = (self.width, self.height)
                self.point_light_shader["proj_const"].value = projection.projection_constants
                self.point_light_shader["radius"].value = light_size
                self.unit_cube.render(self.point_light_shader)

        helper._depth_sampler.clear(location=1)