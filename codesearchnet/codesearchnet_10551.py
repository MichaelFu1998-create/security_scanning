def apply_function(self, func):
        """Apply a function to all grid_stack in the grid-stack.
        
        This is used by the *ray-tracing* module to easily apply tracing operations to all grid_stack."""
        if self.blurring is not None and self.pix is not None:
            return GridStack(func(self.regular), func(self.sub), func(self.blurring), func(self.pix))
        elif self.blurring is None and self.pix is not None:
            return GridStack(func(self.regular), func(self.sub), self.blurring, func(self.pix))
        elif self.blurring is not None and self.pix is None:
            return GridStack(func(self.regular), func(self.sub), func(self.blurring), self.pix)
        else:
            return GridStack(func(self.regular), func(self.sub), self.blurring, self.pix)