def render(self, dt):
        '''Draw all bodies in the world.'''
        for frame in self._frozen:
            for body in frame:
                self.draw_body(body)
        for body in self.world.bodies:
            self.draw_body(body)

        if hasattr(self.world, 'markers'):
            # draw line between anchor1 and anchor2 for marker joints.
            window.glColor4f(0.9, 0.1, 0.1, 0.9)
            window.glLineWidth(3)
            for j in self.world.markers.joints.values():
                window.glBegin(window.GL_LINES)
                window.glVertex3f(*j.getAnchor())
                window.glVertex3f(*j.getAnchor2())
                window.glEnd()