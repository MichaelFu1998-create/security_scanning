def start(self):
        """
        Start connection and initialize session services
        """

        # flush event queue in defensive way
        logger = _get_logger(self.debug)
        started = self._session.start()
        if started:
            ev = self._session.nextEvent()
            ev_name = _EVENT_DICT[ev.eventType()]
            logger.info('Event Type: {!r}'.format(ev_name))
            for msg in ev:
                logger.info('Message Received:\n{}'.format(msg))
            if ev.eventType() != blpapi.Event.SESSION_STATUS:
                raise RuntimeError('Expected a "SESSION_STATUS" event but '
                                   'received a {!r}'.format(ev_name))
            ev = self._session.nextEvent()
            ev_name = _EVENT_DICT[ev.eventType()]
            logger.info('Event Type: {!r}'.format(ev_name))
            for msg in ev:
                logger.info('Message Received:\n{}'.format(msg))
            if ev.eventType() != blpapi.Event.SESSION_STATUS:
                raise RuntimeError('Expected a "SESSION_STATUS" event but '
                                   'received a {!r}'.format(ev_name))
        else:
            ev = self._session.nextEvent(self.timeout)
            if ev.eventType() == blpapi.Event.SESSION_STATUS:
                for msg in ev:
                    logger.warning('Message Received:\n{}'.format(msg))
                raise ConnectionError('Could not start blpapi.Session')
        self._init_services()
        return self