def add_condor_dag(self, token, batchmaketaskid, dagfilename,
                       dagmanoutfilename):
        """
        Add a Condor DAG to the given Batchmake task.

        :param token: A valid token for the user in question.
        :type token: string
        :param batchmaketaskid: id of the Batchmake task for this DAG
        :type batchmaketaskid: int | long
        :param dagfilename: Filename of the DAG file
        :type dagfilename: string
        :param dagmanoutfilename: Filename of the DAG processing output
        :type dagmanoutfilename: string
        :returns: The created Condor DAG DAO
        :rtype: dict
        """
        parameters = dict()
        parameters['token'] = token
        parameters['batchmaketaskid'] = batchmaketaskid
        parameters['dagfilename'] = dagfilename
        parameters['outfilename'] = dagmanoutfilename
        response = self.request('midas.batchmake.add.condor.dag', parameters)
        return response