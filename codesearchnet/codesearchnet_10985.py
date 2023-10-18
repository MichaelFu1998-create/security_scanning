def combine(self):
        """Combine diffuse and light buffer"""
        self.gbuffer.color_attachments[0].use(location=0)
        self.combine_shader["diffuse_buffer"].value = 0
        self.lightbuffer.color_attachments[0].use(location=1)
        self.combine_shader["light_buffer"].value = 1
        self.quad.render(self.combine_shader)