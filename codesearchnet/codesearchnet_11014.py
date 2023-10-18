def load(self):
        """Deferred loading"""
        path = self.find_scene(self.meta.path)

        if not path:
            raise ValueError("Scene '{}' not found".format(self.meta.path))

        if path.suffix == '.bin':
            path = path.parent / path.stem

        data = pywavefront.Wavefront(str(path), create_materials=True, cache=True)
        scene = Scene(self.meta.resolved_path)
        texture_cache = {}

        for _, mat in data.materials.items():
            mesh = Mesh(mat.name)

            # Traditional loader
            if mat.vertices:
                buffer_format, attributes, mesh_attributes = translate_buffer_format(mat.vertex_format)
                vbo = numpy.array(mat.vertices, dtype='f4')

                vao = VAO(mat.name, mode=moderngl.TRIANGLES)
                vao.buffer(vbo, buffer_format, attributes)
                mesh.vao = vao

                for attrs in mesh_attributes:
                    mesh.add_attribute(*attrs)

            # Binary cache loader
            elif hasattr(mat, 'vao'):
                mesh = Mesh(mat.name)
                mesh.vao = mat.vao
                for attrs in mat.mesh_attributes:
                    mesh.add_attribute(*attrs)
            else:
                # Empty
                continue

            scene.meshes.append(mesh)

            mesh.material = Material(mat.name)
            scene.materials.append(mesh.material)
            mesh.material.color = mat.diffuse

            if mat.texture:
                # A texture can be referenced multiple times, so we need to cache loaded ones
                texture = texture_cache.get(mat.texture.path)
                if not texture:
                    print("Loading:", mat.texture.path)
                    texture = textures.load(TextureDescription(
                        label=mat.texture.path,
                        path=mat.texture.path,
                        mipmap=True,
                    ))
                    texture_cache[mat.texture.path] = texture

                mesh.material.mat_texture = MaterialTexture(
                    texture=texture,
                    sampler=None,
                )

            node = Node(mesh=mesh)
            scene.root_nodes.append(node)

        # Not supported yet for obj
        # self.calc_scene_bbox()
        scene.prepare()

        return scene