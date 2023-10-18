def ancestors(self):
        """Returns list of ancestor task specs based on inputs"""
        results = []

        def recursive_find_ancestors(task, stack):
            for input in task.inputs:
                if input not in stack:
                    stack.append(input)
                    recursive_find_ancestors(input, stack)
        recursive_find_ancestors(self, results)

        return results