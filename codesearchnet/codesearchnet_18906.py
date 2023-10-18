def add_condor_job(self, token, batchmaketaskid, jobdefinitionfilename,
                       outputfilename, errorfilename, logfilename,
                       postfilename):
        """
        Add a Condor DAG job to the Condor DAG associated with this
        Batchmake task

        :param token: A valid token for the user in question.
        :type token: string
        :param batchmaketaskid: id of the Batchmake task for this DAG
        :type batchmaketaskid: int | long
        :param jobdefinitionfilename: Filename of the definition file for the
            job
        :type jobdefinitionfilename: string
        :param outputfilename: Filename of the output file for the job
        :type outputfilename: string
        :param errorfilename: Filename of the error file for the job
        :type errorfilename: string
        :param logfilename: Filename of the log file for the job
        :type logfilename: string
        :param postfilename: Filename of the post script log file for the job
        :type postfilename: string
        :return: The created Condor job DAO.
        :rtype: dict
        """
        parameters = dict()
        parameters['token'] = token
        parameters['batchmaketaskid'] = batchmaketaskid
        parameters['jobdefinitionfilename'] = jobdefinitionfilename
        parameters['outputfilename'] = outputfilename
        parameters['errorfilename'] = errorfilename
        parameters['logfilename'] = logfilename
        parameters['postfilename'] = postfilename
        response = self.request('midas.batchmake.add.condor.job', parameters)
        return response