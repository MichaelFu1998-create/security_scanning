def from_separate(cls, meta: ProgramDescription, vertex_source, geometry_source=None, fragment_source=None,
                      tess_control_source=None, tess_evaluation_source=None):
        """Initialize multiple shader strings"""
        instance = cls(meta)
        instance.vertex_source = ShaderSource(
            VERTEX_SHADER,
            meta.path or meta.vertex_shader,
            vertex_source,
        )

        if geometry_source:
            instance.geometry_source = ShaderSource(
                GEOMETRY_SHADER,
                meta.path or meta.geometry_shader,
                geometry_source,
            )

        if fragment_source:
            instance.fragment_source = ShaderSource(
                FRAGMENT_SHADER,
                meta.path or meta.fragment_shader,
                fragment_source,
            )

        if tess_control_source:
            instance.tess_control_source = ShaderSource(
                TESS_CONTROL_SHADER,
                meta.path or meta.tess_control_shader,
                tess_control_source,
            )

        if tess_evaluation_source:
            instance.tess_evaluation_source = ShaderSource(
                TESS_EVALUATION_SHADER,
                meta.path or meta.tess_control_shader,
                tess_evaluation_source,
            )

        return instance