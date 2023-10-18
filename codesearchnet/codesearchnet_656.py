def save_model(self, network=None, model_name='model', **kwargs):
        """Save model architecture and parameters into database, timestamp will be added automatically.

        Parameters
        ----------
        network : TensorLayer layer
            TensorLayer layer instance.
        model_name : str
            The name/key of model.
        kwargs : other events
            Other events, such as name, accuracy, loss, step number and etc (optinal).

        Examples
        ---------
        Save model architecture and parameters into database.
        >>> db.save_model(net, accuracy=0.8, loss=2.3, name='second_model')

        Load one model with parameters from database (run this in other script)
        >>> net = db.find_top_model(sess=sess, accuracy=0.8, loss=2.3)

        Find and load the latest model.
        >>> net = db.find_top_model(sess=sess, sort=[("time", pymongo.DESCENDING)])
        >>> net = db.find_top_model(sess=sess, sort=[("time", -1)])

        Find and load the oldest model.
        >>> net = db.find_top_model(sess=sess, sort=[("time", pymongo.ASCENDING)])
        >>> net = db.find_top_model(sess=sess, sort=[("time", 1)])

        Get model information
        >>> net._accuracy
        ... 0.8

        Returns
        ---------
        boolean : True for success, False for fail.
        """
        kwargs.update({'model_name': model_name})
        self._fill_project_info(kwargs)  # put project_name into kwargs

        params = network.get_all_params()

        s = time.time()

        kwargs.update({'architecture': network.all_graphs, 'time': datetime.utcnow()})

        try:
            params_id = self.model_fs.put(self._serialization(params))
            kwargs.update({'params_id': params_id, 'time': datetime.utcnow()})
            self.db.Model.insert_one(kwargs)
            print("[Database] Save model: SUCCESS, took: {}s".format(round(time.time() - s, 2)))
            return True
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logging.info("{}  {}  {}  {}  {}".format(exc_type, exc_obj, fname, exc_tb.tb_lineno, e))
            print("[Database] Save model: FAIL")
            return False