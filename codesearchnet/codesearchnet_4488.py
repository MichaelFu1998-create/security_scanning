def write_state_file(self):
        """Save information that must persist to a file.

        We do not want to create a new VPC and new identical security groups, so we save
        information about them in a file between runs.
        """
        fh = open('awsproviderstate.json', 'w')
        state = {}
        state['vpcID'] = self.vpc_id
        state['sgID'] = self.sg_id
        state['snIDs'] = self.sn_ids
        state['instances'] = self.instances
        state["instanceState"] = self.instance_states
        fh.write(json.dumps(state, indent=4))