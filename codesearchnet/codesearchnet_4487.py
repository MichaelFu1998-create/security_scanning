def read_state_file(self, state_file):
        """Read the state file, if it exists.

        If this script has been run previously, resource IDs will have been written to a
        state file. On starting a run, a state file will be looked for before creating new
        infrastructure. Information on VPCs, security groups, and subnets are saved, as
        well as running instances and their states.

        AWS has a maximum number of VPCs per region per account, so we do not want to
        clutter users' AWS accounts with security groups and VPCs that will be used only
        once.
        """
        try:
            fh = open(state_file, 'r')
            state = json.load(fh)
            self.vpc_id = state['vpcID']
            self.sg_id = state['sgID']
            self.sn_ids = state['snIDs']
            self.instances = state['instances']
        except Exception as e:
            logger.debug("Caught exception while reading state file: {0}".format(e))
            raise e
        logger.debug("Done reading state from the local state file.")