def create_joints(self):
        '''Traverse the bone hierarchy and create physics joints.'''
        stack = ['root']
        while stack:
            parent = stack.pop()
            for child in self.hierarchy.get(parent, ()):
                stack.append(child)
            if parent not in self.bones:
                continue
            bone = self.bones[parent]
            body = [b for b in self.bodies if b.name == parent][0]
            for child in self.hierarchy.get(parent, ()):
                child_bone = self.bones[child]
                child_body = [b for b in self.bodies if b.name == child][0]
                shape = ('', 'hinge', 'universal', 'ball')[len(child_bone.dof)]
                self.joints.append(self.world.join(shape, body, child_body))