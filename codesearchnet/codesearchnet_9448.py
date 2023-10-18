def release(self):
        """
        Release, incrementing the internal counter by one.
        """
        if self.value is not None:
            self.value += 1
            if self.value > self.maximum_value:
                raise ValueError("Too many releases")