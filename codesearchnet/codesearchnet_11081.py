def from_single(cls, meta: ProgramDescription, source: str):
        """Initialize a single glsl string containing all shaders"""
        instance = cls(meta)
        instance.vertex_source = ShaderSource(
            VERTEX_SHADER,
            meta.path or meta.vertex_shader,
            source
        )

        if GEOMETRY_SHADER in source:
            instance.geometry_source = ShaderSource(
                GEOMETRY_SHADER,
                meta.path or meta.geometry_shader,
                source,
            )

        if FRAGMENT_SHADER in source:
            instance.fragment_source = ShaderSource(
                FRAGMENT_SHADER,
                meta.path or meta.fragment_shader,
                source,
            )

        if TESS_CONTROL_SHADER in source:
            instance.tess_control_source = ShaderSource(
                TESS_CONTROL_SHADER,
                meta.path or meta.tess_control_shader,
                source,
            )

        if TESS_EVALUATION_SHADER in source:
            instance.tess_evaluation_source = ShaderSource(
                TESS_EVALUATION_SHADER,
                meta.path or meta.tess_evaluation_shader,
                source,
            )

        return instance