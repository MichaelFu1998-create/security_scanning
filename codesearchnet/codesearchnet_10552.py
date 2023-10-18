def map_function(self, func, *arg_lists):
        """Map a function to all grid_stack in a grid-stack"""
        return GridStack(*[func(*args) for args in zip(self, *arg_lists)])