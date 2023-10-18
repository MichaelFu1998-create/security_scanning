def show_summary(self):
        """Print human readable summary of current AWS state to log and to console."""
        self.get_instance_state()
        status_string = "EC2 Summary:\n\tVPC IDs: {}\n\tSubnet IDs: \
{}\n\tSecurity Group ID: {}\n\tRunning Instance IDs: {}\n".format(
            self.vpc_id, self.sn_ids, self.sg_id, self.instances
        )
        status_string += "\tInstance States:\n\t\t"
        self.get_instance_state()
        for state in self.instance_states.keys():
            status_string += "Instance ID: {}  State: {}\n\t\t".format(
                state, self.instance_states[state]
            )
        status_string += "\n"
        logger.info(status_string)
        return status_string