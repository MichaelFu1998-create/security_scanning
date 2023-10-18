def forloop(self, range, ordered=False, schedule=('static', 1)):
        """ schedule can be
            (sch, chunk) or sch;
            sch is 'static', 'dynamic' or 'guided'.

            chunk defaults to 1

            if ordered, create an ordred
        """

        if isinstance(schedule, tuple):
            schedule, chunk = schedule
        else:
            chunk = None
        if schedule == 'static':
            return self._StaticForLoop(range, ordered, chunk)
        elif schedule == 'dynamic':
            return self._DynamicForLoop(range, ordered, chunk, guided=False)
        elif schedule == 'guided':
            return self._DynamicForLoop(range, ordered, chunk, guided=True)
        else:
            raise "schedule unknown"