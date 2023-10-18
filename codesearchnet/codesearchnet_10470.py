def grid_stack_from_deflection_stack(grid_stack, deflection_stack):
    """For a deflection stack, comput a new grid stack but subtracting the deflections"""

    if deflection_stack is not None:
        def minus(grid, deflections):
            return grid - deflections

        return grid_stack.map_function(minus, deflection_stack)