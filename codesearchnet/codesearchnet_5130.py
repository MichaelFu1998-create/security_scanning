def change_kernel(self, kernel, return_dict=True):
        """Change the kernel to a new one

        Args:
            kernel : instance of digitalocean.Kernel.Kernel

        Optional Args:
            return_dict (bool): Return a dict when True (default),
                otherwise return an Action.

        Returns dict or Action
        """
        if type(kernel) != Kernel:
            raise BadKernelObject("Use Kernel object")

        return self._perform_action(
            {'type': 'change_kernel', 'kernel': kernel.id},
            return_dict
        )