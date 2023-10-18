def set_data(self, **kwargs):
        """
        Defines the given data field(s) using the given name/value pairs.
        """
        for key in kwargs:
            if key in self.defines:
                msg = "Spec data %s can not be modified" % key
                raise WorkflowException(self, msg)
        self.data.update(kwargs)