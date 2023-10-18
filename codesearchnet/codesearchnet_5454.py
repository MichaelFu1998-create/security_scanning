def has_fired(self, my_task):
        """
        The Timer is considered to have fired if the evaluated dateTime
        expression is before datetime.datetime.now()
        """
        dt = my_task.workflow.script_engine.evaluate(my_task, self.dateTime)
        if dt is None:
            return False
        if dt.tzinfo:
            tz = dt.tzinfo
            now = tz.fromutc(datetime.datetime.utcnow().replace(tzinfo=tz))
        else:
            now = datetime.datetime.now()
        return now > dt