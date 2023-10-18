def find_top_model(self, sess, sort=None, model_name='model', **kwargs):
        """Finds and returns a model architecture and its parameters from the database which matches the requirement.

        Parameters
        ----------
        sess : Session
            TensorFlow session.
        sort : List of tuple
            PyMongo sort comment, search "PyMongo find one sorting" and `collection level operations <http://api.mongodb.com/python/current/api/pymongo/collection.html>`__ for more details.
        model_name : str or None
            The name/key of model.
        kwargs : other events
            Other events, such as name, accuracy, loss, step number and etc (optinal).

        Examples
        ---------
        - see ``save_model``.

        Returns
        ---------
        network : TensorLayer layer
            Note that, the returned network contains all information of the document (record), e.g. if you saved accuracy in the document, you can get the accuracy by using ``net._accuracy``.
        """
        # print(kwargs)   # {}
        kwargs.update({'model_name': model_name})
        self._fill_project_info(kwargs)

        s = time.time()

        d = self.db.Model.find_one(filter=kwargs, sort=sort)

        _temp_file_name = '_find_one_model_ztemp_file'
        if d is not None:
            params_id = d['params_id']
            graphs = d['architecture']
            _datetime = d['time']
            exists_or_mkdir(_temp_file_name, False)
            with open(os.path.join(_temp_file_name, 'graph.pkl'), 'wb') as file:
                pickle.dump(graphs, file, protocol=pickle.HIGHEST_PROTOCOL)
        else:
            print("[Database] FAIL! Cannot find model: {}".format(kwargs))
            return False
        try:
            params = self._deserialization(self.model_fs.get(params_id).read())
            np.savez(os.path.join(_temp_file_name, 'params.npz'), params=params)

            network = load_graph_and_params(name=_temp_file_name, sess=sess)
            del_folder(_temp_file_name)

            pc = self.db.Model.find(kwargs)
            print(
                "[Database] Find one model SUCCESS. kwargs:{} sort:{} save time:{} took: {}s".
                format(kwargs, sort, _datetime, round(time.time() - s, 2))
            )

            # put all informations of model into the TL layer
            for key in d:
                network.__dict__.update({"_%s" % key: d[key]})

            # check whether more parameters match the requirement
            params_id_list = pc.distinct('params_id')
            n_params = len(params_id_list)
            if n_params != 1:
                print("     Note that there are {} models match the kwargs".format(n_params))
            return network
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logging.info("{}  {}  {}  {}  {}".format(exc_type, exc_obj, fname, exc_tb.tb_lineno, e))
            return False