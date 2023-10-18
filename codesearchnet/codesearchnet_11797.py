def get_tasks(self):
        """
        Returns an ordered list of all task names.
        """
        tasks = set(self.tasks)#DEPRECATED
        for _name in dir(self):
            # Skip properties so we don't accidentally execute any methods.
            if isinstance(getattr(type(self), _name, None), property):
                continue
            attr = getattr(self, _name)
            if hasattr(attr, '__call__') and getattr(attr, 'is_task', False):
                tasks.add(_name)
        return sorted(tasks)