def load_shader(self, shader_type: str, path: str):
        """Load a single shader"""
        if path:
            resolved_path = self.find_program(path)
            if not resolved_path:
                raise ValueError("Cannot find {} shader '{}'".format(shader_type, path))

            print("Loading:", path)

            with open(resolved_path, 'r') as fd:
                return fd.read()