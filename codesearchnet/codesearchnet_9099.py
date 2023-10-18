def _init_services(self):
        """
        Initialize blpapi.Session services
        """
        logger = _get_logger(self.debug)

        # flush event queue in defensive way
        opened = self._session.openService('//blp/refdata')
        ev = self._session.nextEvent()
        ev_name = _EVENT_DICT[ev.eventType()]
        logger.info('Event Type: {!r}'.format(ev_name))
        for msg in ev:
            logger.info('Message Received:\n{}'.format(msg))
        if ev.eventType() != blpapi.Event.SERVICE_STATUS:
            raise RuntimeError('Expected a "SERVICE_STATUS" event but '
                               'received a {!r}'.format(ev_name))
        if not opened:
            logger.warning('Failed to open //blp/refdata')
            raise ConnectionError('Could not open a //blp/refdata service')
        self.refDataService = self._session.getService('//blp/refdata')

        opened = self._session.openService('//blp/exrsvc')
        ev = self._session.nextEvent()
        ev_name = _EVENT_DICT[ev.eventType()]
        logger.info('Event Type: {!r}'.format(ev_name))
        for msg in ev:
            logger.info('Message Received:\n{}'.format(msg))
        if ev.eventType() != blpapi.Event.SERVICE_STATUS:
            raise RuntimeError('Expected a "SERVICE_STATUS" event but '
                               'received a {!r}'.format(ev_name))
        if not opened:
            logger.warning('Failed to open //blp/exrsvc')
            raise ConnectionError('Could not open a //blp/exrsvc service')
        self.exrService = self._session.getService('//blp/exrsvc')

        return self