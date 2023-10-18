def create_task(self):
        """
        Create an instance of the task appropriately. A subclass can override
        this method to get extra information from the node.
        """
        return self.spec_class(self.spec, self.get_task_spec_name(),
                               lane=self.get_lane(),
                               description=self.node.get('name', None))