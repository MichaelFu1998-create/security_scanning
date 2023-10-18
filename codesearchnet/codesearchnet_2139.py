def get_named_tensor(self, name):
        """
        Returns a named tensor if available.

        Returns:
            valid: True if named tensor found, False otherwise
            tensor: If valid, will be a tensor, otherwise None
        """
        if name in self.named_tensors:
            return True, self.named_tensors[name]
        else:
            return False, None