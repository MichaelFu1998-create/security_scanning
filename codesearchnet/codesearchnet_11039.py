def _init_depth_texture_draw(self):
        """Initialize geometry and shader for drawing FBO layers"""
        from demosys import geometry

        if not TextureHelper._quad:
            TextureHelper._quad = geometry.quad_fs()

        # Shader for drawing depth layers
        TextureHelper._depth_shader = context.ctx().program(
            vertex_shader="""
                #version 330

                in vec3 in_position;
                in vec2 in_uv;
                out vec2 uv;
                uniform vec2 offset;
                uniform vec2 scale;

                void main() {
                    uv = in_uv;
                    gl_Position = vec4((in_position.xy + vec2(1.0, 1.0)) * scale + offset, 0.0, 1.0);
                }
            """,
            fragment_shader="""
                #version 330

                out vec4 out_color;
                in vec2 uv;
                uniform sampler2D texture0;
                uniform float near;
                uniform float far;

                void main() {
                    float z = texture(texture0, uv).r;
                    float d = (2.0 * near) / (far + near - z * (far - near));
                    out_color = vec4(d);
                }
            """
        )

        TextureHelper._depth_sampler = self.ctx.sampler(
            filter=(moderngl.LINEAR, moderngl.LINEAR),
            compare_func='',
        )