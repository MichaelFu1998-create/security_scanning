def create_bodies(self, translate=(0, 1, 0), size=0.1):
        '''Traverse the bone hierarchy and create physics bodies.'''
        stack = [('root', 0, self.root['position'] + translate)]
        while stack:
            name, depth, end = stack.pop()

            for child in self.hierarchy.get(name, ()):
                stack.append((child, depth + 1, end + self.bones[child].end))

            if name not in self.bones:
                continue

            bone = self.bones[name]
            body = self.world.create_body(
                'box', name=bone.name, density=self.density,
                lengths=(size, size, bone.length))
            body.color = self.color

            # move the center of the body to the halfway point between
            # the parent (joint) and child (joint).
            x, y, z = end - bone.direction * bone.length / 2

            # swizzle y and z -- asf uses y as up, but we use z as up.
            body.position = x, z, y

            # compute an orthonormal (rotation) matrix using the ground and
            # the body. this is mind-bending but seems to work.
            u = bone.direction
            v = np.cross(u, [0, 1, 0])
            l = np.linalg.norm(v)
            if l > 0:
                v /= l
                rot = np.vstack([np.cross(u, v), v, u]).T
                swizzle = [[1, 0, 0], [0, 0, 1], [0, -1, 0]]
                body.rotation = np.dot(swizzle, rot)

            self.bodies.append(body)