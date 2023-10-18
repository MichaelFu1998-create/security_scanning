def attach(self, frame_no):
        '''Attach marker bodies to the corresponding skeleton bodies.

        Attachments are only made for markers that are not in a dropout state in
        the given frame.

        Parameters
        ----------
        frame_no : int
            The frame of data we will use for attaching marker bodies.
        '''
        assert not self.joints
        for label, j in self.channels.items():
            target = self.targets.get(label)
            if target is None:
                continue
            if self.visibility[frame_no, j] < 0:
                continue
            if np.linalg.norm(self.velocities[frame_no, j]) > 10:
                continue
            joint = ode.BallJoint(self.world.ode_world, self.jointgroup)
            joint.attach(self.bodies[label].ode_body, target.ode_body)
            joint.setAnchor1Rel([0, 0, 0])
            joint.setAnchor2Rel(self.offsets[label])
            joint.setParam(ode.ParamCFM, self.cfms[frame_no, j])
            joint.setParam(ode.ParamERP, self.erp)
            joint.name = label
            self.joints[label] = joint
        self._frame_no = frame_no