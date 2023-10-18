def bsrch(self, domain):
        """
        This function uses the Bloomberg API to retrieve 'bsrch' (Bloomberg
        SRCH Data) queries. Returns list of tickers.

        Parameters
        ----------
        domain: string
            A character string with the name of the domain to execute.
            It can be a user defined SRCH screen, commodity screen or
            one of the variety of Bloomberg examples. All domains are in the
            format <domain>:<search_name>. Example "COMDTY:NGFLOW"

        Returns
        -------
        data: pandas.DataFrame
            List of bloomberg tickers from the BSRCH
        """
        logger = _get_logger(self.debug)
        request = self.exrService.createRequest('ExcelGetGridRequest')
        request.set('Domain', domain)
        logger.info('Sending Request:\n{}'.format(request))
        self._session.sendRequest(request, identity=self._identity)
        data = []
        for msg in self._receive_events(to_dict=False):
            for v in msg.getElement("DataRecords").values():
                for f in v.getElement("DataFields").values():
                    data.append(f.getElementAsString("StringValue"))
        return pd.DataFrame(data)