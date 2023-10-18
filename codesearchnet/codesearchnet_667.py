def create_task(self, task_name=None, script=None, hyper_parameters=None, saved_result_keys=None, **kwargs):
        """Uploads a task to the database, timestamp will be added automatically.

        Parameters
        -----------
        task_name : str
            The task name.
        script : str
            File name of the python script.
        hyper_parameters : dictionary
            The hyper parameters pass into the script.
        saved_result_keys : list of str
            The keys of the task results to keep in the database when the task finishes.
        kwargs : other parameters
            Users customized parameters such as description, version number.

        Examples
        -----------
        Uploads a task
        >>> db.create_task(task_name='mnist', script='example/tutorial_mnist_simple.py', description='simple tutorial')

        Finds and runs the latest task
        >>> db.run_top_task(sess=sess, sort=[("time", pymongo.DESCENDING)])
        >>> db.run_top_task(sess=sess, sort=[("time", -1)])

        Finds and runs the oldest task
        >>> db.run_top_task(sess=sess, sort=[("time", pymongo.ASCENDING)])
        >>> db.run_top_task(sess=sess, sort=[("time", 1)])

        """
        if not isinstance(task_name, str):  # is None:
            raise Exception("task_name should be string")
        if not isinstance(script, str):  # is None:
            raise Exception("script should be string")
        if hyper_parameters is None:
            hyper_parameters = {}
        if saved_result_keys is None:
            saved_result_keys = []

        self._fill_project_info(kwargs)
        kwargs.update({'time': datetime.utcnow()})
        kwargs.update({'hyper_parameters': hyper_parameters})
        kwargs.update({'saved_result_keys': saved_result_keys})

        _script = open(script, 'rb').read()

        kwargs.update({'status': 'pending', 'script': _script, 'result': {}})
        self.db.Task.insert_one(kwargs)
        logging.info("[Database] Saved Task - task_name: {} script: {}".format(task_name, script))