def execute(self, task, script, **kwargs):
        """
        Execute the script, within the context of the specified task
        """
        locals().update(kwargs)
        exec(script)