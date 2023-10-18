def shut_down_instance(self, instances=None):
        """Shut down a list of instances, if provided.

        If no instance is provided, the last instance started up will be shut down.
        """

        if instances and len(self.instances) > 0:
            print(instances)
            try:
                print([i.id for i in instances])
            except Exception as e:
                print(e)
            term = self.client.terminate_instances(InstanceIds=instances)
            logger.info("Shut down {} instances (ids:{}".format(len(instances), str(instances)))
        elif len(self.instances) > 0:
            instance = self.instances.pop()
            term = self.client.terminate_instances(InstanceIds=[instance])
            logger.info("Shut down 1 instance (id:{})".format(instance))
        else:
            logger.warn("No Instances to shut down.\n")
            return -1
        self.get_instance_state()
        return term