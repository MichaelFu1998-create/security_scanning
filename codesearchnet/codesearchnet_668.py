def run_top_task(self, task_name=None, sort=None, **kwargs):
        """Finds and runs a pending task that in the first of the sorting list.

        Parameters
        -----------
        task_name : str
            The task name.
        sort : List of tuple
            PyMongo sort comment, search "PyMongo find one sorting" and `collection level operations <http://api.mongodb.com/python/current/api/pymongo/collection.html>`__ for more details.
        kwargs : other parameters
            Users customized parameters such as description, version number.

        Examples
        ---------
        Monitors the database and pull tasks to run
        >>> while True:
        >>>     print("waiting task from distributor")
        >>>     db.run_top_task(task_name='mnist', sort=[("time", -1)])
        >>>     time.sleep(1)

        Returns
        --------
        boolean : True for success, False for fail.
        """
        if not isinstance(task_name, str):  # is None:
            raise Exception("task_name should be string")
        self._fill_project_info(kwargs)
        kwargs.update({'status': 'pending'})

        # find task and set status to running
        task = self.db.Task.find_one_and_update(kwargs, {'$set': {'status': 'running'}}, sort=sort)

        try:
            # get task info e.g. hyper parameters, python script
            if task is None:
                logging.info("[Database] Find Task FAIL: key: {} sort: {}".format(task_name, sort))
                return False
            else:
                logging.info("[Database] Find Task SUCCESS: key: {} sort: {}".format(task_name, sort))
            _datetime = task['time']
            _script = task['script']
            _id = task['_id']
            _hyper_parameters = task['hyper_parameters']
            _saved_result_keys = task['saved_result_keys']
            logging.info("  hyper parameters:")
            for key in _hyper_parameters:
                globals()[key] = _hyper_parameters[key]
                logging.info("    {}: {}".format(key, _hyper_parameters[key]))
            # run task
            s = time.time()
            logging.info("[Database] Start Task: key: {} sort: {} push time: {}".format(task_name, sort, _datetime))
            _script = _script.decode('utf-8')
            with tf.Graph().as_default():  # as graph: # clear all TF graphs
                exec(_script, globals())

            # set status to finished
            _ = self.db.Task.find_one_and_update({'_id': _id}, {'$set': {'status': 'finished'}})

            # return results
            __result = {}
            for _key in _saved_result_keys:
                logging.info("  result: {}={} {}".format(_key, globals()[_key], type(globals()[_key])))
                __result.update({"%s" % _key: globals()[_key]})
            _ = self.db.Task.find_one_and_update(
                {
                    '_id': _id
                }, {'$set': {
                    'result': __result
                }}, return_document=pymongo.ReturnDocument.AFTER
            )
            logging.info(
                "[Database] Finished Task: task_name - {} sort: {} push time: {} took: {}s".
                format(task_name, sort, _datetime,
                       time.time() - s)
            )
            return True
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logging.info("{}  {}  {}  {}  {}".format(exc_type, exc_obj, fname, exc_tb.tb_lineno, e))
            logging.info("[Database] Fail to run task")
            # if fail, set status back to pending
            _ = self.db.Task.find_one_and_update({'_id': _id}, {'$set': {'status': 'pending'}})
            return False