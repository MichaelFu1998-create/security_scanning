def construct(cls, project, *, run=None, name=None, data=None, **desc):
        """
        Construct an animation, set the runner, and add in the two
        "reserved fields" `name` and `data`.
        """
        from . failed import Failed
        exception = desc.pop('_exception', None)
        if exception:
            a = Failed(project.layout, desc, exception)
        else:
            try:
                a = cls(project.layout, **desc)
                a._set_runner(run or {})
            except Exception as e:
                if cls.FAIL_ON_EXCEPTION:
                    raise
                a = Failed(project.layout, desc, e)

        a.name = name
        a.data = data
        return a