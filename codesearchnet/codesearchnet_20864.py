def joint_torques(self):
        '''Get a list of all current joint torques in the skeleton.'''
        return as_flat_array(getattr(j, 'amotor', j).feedback[-1][:j.ADOF]
                             for j in self.joints)