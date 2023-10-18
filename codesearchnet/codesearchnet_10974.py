def apply_mesh_programs(self, mesh_programs=None):
        """Applies mesh programs to meshes"""
        if not mesh_programs:
            mesh_programs = [ColorProgram(), TextureProgram(), FallbackProgram()]

        for mesh in self.meshes:
            for mp in mesh_programs:
                instance = mp.apply(mesh)
                if instance is not None:
                    if isinstance(instance, MeshProgram):
                        mesh.mesh_program = mp
                        break
                    else:
                        raise ValueError("apply() must return a MeshProgram instance, not {}".format(type(instance)))

            if not mesh.mesh_program:
                print("WARING: No mesh program applied to '{}'".format(mesh.name))