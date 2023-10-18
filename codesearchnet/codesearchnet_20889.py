def forward_dynamics(self, torques, start=0, states=None):
        '''Move the body according to a set of torque data.'''
        if states is not None:
            self.skeleton.set_body_states(states)
        for frame_no, torque in enumerate(torques):
            if frame_no < start:
                continue
            if frame_no >= end:
                break
            self.ode_space.collide(None, self.on_collision)
            self.skeleton.add_torques(torque)
            self.ode_world.step(self.dt)
            yield
            self.ode_contactgroup.empty()