def bdib(self, ticker, start_datetime, end_datetime, event_type, interval,
             elms=None):
        """
        Get Open, High, Low, Close, Volume, and numEvents for a ticker.
        Return pandas DataFrame

        Parameters
        ----------
        ticker: string
            String corresponding to ticker
        start_datetime: string
            UTC datetime in format YYYY-mm-ddTHH:MM:SS
        end_datetime: string
            UTC datetime in format YYYY-mm-ddTHH:MM:SS
        event_type: string {TRADE, BID, ASK, BID_BEST, ASK_BEST, BEST_BID,
                           BEST_ASK}
            Requested data event type
        interval: int {1... 1440}
            Length of time bars
        elms: list of tuples
            List of tuples where each tuple corresponds to the other elements
            to be set. Refer to the IntradayBarRequest section in the
            'Services & schemas reference guide' for more info on these values
        """
        elms = [] if not elms else elms

        # flush event queue in case previous call errored out
        logger = _get_logger(self.debug)
        while(self._session.tryNextEvent()):
            pass

        # Create and fill the request for the historical data
        request = self.refDataService.createRequest('IntradayBarRequest')
        request.set('security', ticker)
        request.set('eventType', event_type)
        request.set('interval', interval)  # bar interval in minutes
        request.set('startDateTime', start_datetime)
        request.set('endDateTime', end_datetime)
        for name, val in elms:
            request.set(name, val)

        logger.info('Sending Request:\n{}'.format(request))
        # Send the request
        self._session.sendRequest(request, identity=self._identity)
        # Process received events
        data = []
        flds = ['open', 'high', 'low', 'close', 'volume', 'numEvents']
        for msg in self._receive_events():
            d = msg['element']['IntradayBarResponse']
            for bar in d['barData']['barTickData']:
                data.append(bar['barTickData'])
        data = pd.DataFrame(data).set_index('time').sort_index().loc[:, flds]
        return data