def fetch_data(self, return_header=False):
        """Fetches data from the queue.

        Parameters
        ----------
        return_header : bool (optonal, default: ``False``)
            Determines whether the column headers are returned.

        Returns
        -------
        data : :class:`~numpy.ndarray`
            A six column :class:`~numpy.ndarray` of all the data. The
            columns are:

            * 1st: The arrival time of an agent.
            * 2nd: The service start time of an agent.
            * 3rd: The departure time of an agent.
            * 4th: The length of the queue upon the agents arrival.
            * 5th: The total number of :class:`Agents<.Agent>` in the
              :class:`.QueueServer`.
            * 6th: The :class:`QueueServer's<.QueueServer>` edge index.

        headers : str (optional)
            A comma seperated string of the column headers. Returns
            ``'arrival,service,departure,num_queued,num_total,q_id'``
        """

        qdata = []
        for d in self.data.values():
            qdata.extend(d)

        dat = np.zeros((len(qdata), 6))
        if len(qdata) > 0:
            dat[:, :5] = np.array(qdata)
            dat[:, 5] = self.edge[2]

            dType = [
                ('a', float),
                ('s', float),
                ('d', float),
                ('q', float),
                ('n', float),
                ('id', float)
            ]
            dat = np.array([tuple(d) for d in dat], dtype=dType)
            dat = np.sort(dat, order='a')
            dat = np.array([tuple(d) for d in dat])

        if return_header:
            return dat, 'arrival,service,departure,num_queued,num_total,q_id'

        return dat