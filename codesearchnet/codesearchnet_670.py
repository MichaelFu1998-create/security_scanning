def check_unfinished_task(self, task_name=None, **kwargs):
        """Finds and runs a pending task.

        Parameters
        -----------
        task_name : str
            The task name.
        kwargs : other parameters
            Users customized parameters such as description, version number.

        Examples
        ---------
        Wait until all tasks finish in user's local console

        >>> while not db.check_unfinished_task():
        >>>     time.sleep(1)
        >>> print("all tasks finished")
        >>> sess = tf.InteractiveSession()
        >>> net = db.find_top_model(sess=sess, sort=[("test_accuracy", -1)])
        >>> print("the best accuracy {} is from model {}".format(net._test_accuracy, net._name))

        Returns
        --------
        boolean : True for success, False for fail.

        """

        if not isinstance(task_name, str):  # is None:
            raise Exception("task_name should be string")
        self._fill_project_info(kwargs)

        kwargs.update({'$or': [{'status': 'pending'}, {'status': 'running'}]})

        # ## find task
        # task = self.db.Task.find_one(kwargs)
        task = self.db.Task.find(kwargs)

        task_id_list = task.distinct('_id')
        n_task = len(task_id_list)

        if n_task == 0:
            logging.info("[Database] No unfinished task - task_name: {}".format(task_name))
            return False
        else:

            logging.info("[Database] Find {} unfinished task - task_name: {}".format(n_task, task_name))
            return True