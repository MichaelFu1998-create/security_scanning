def _gather_all_deps(self, args, kwargs):
        """Count the number of unresolved futures on which a task depends.

        Args:
            - args (List[args]) : The list of args list to the fn
            - kwargs (Dict{kwargs}) : The dict of all kwargs passed to the fn

        Returns:
            - count, [list of dependencies]

        """
        # Check the positional args
        depends = []
        count = 0
        for dep in args:
            if isinstance(dep, Future):
                if self.tasks[dep.tid]['status'] not in FINAL_STATES:
                    count += 1
                depends.extend([dep])

        # Check for explicit kwargs ex, fu_1=<fut>
        for key in kwargs:
            dep = kwargs[key]
            if isinstance(dep, Future):
                if self.tasks[dep.tid]['status'] not in FINAL_STATES:
                    count += 1
                depends.extend([dep])

        # Check for futures in inputs=[<fut>...]
        for dep in kwargs.get('inputs', []):
            if isinstance(dep, Future):
                if self.tasks[dep.tid]['status'] not in FINAL_STATES:
                    count += 1
                depends.extend([dep])

        return count, depends