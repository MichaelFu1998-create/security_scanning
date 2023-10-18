def run(self):
        """The thread function. Calls `self.run()` and if it raises
        an exception, stores it in self.exc_info and exc_queue
        """
        logger.debug("{0}: entering thread".format(self.name))
        while True:
            try:
                self.event_dispatcher.loop()
            except Exception: # pylint: disable-msg=W0703
                self.exc_info = sys.exc_info()
                logger.debug(u"exception in the {0!r} thread:"
                                .format(self.name), exc_info = self.exc_info)
                if self.exc_queue:
                    self.exc_queue.put( (self, self.exc_info) )
                    continue
                else:
                    logger.debug("{0}: aborting thread".format(self.name))
                    return
            except:
                logger.debug("{0}: aborting thread".format(self.name))
                return
            break
        logger.debug("{0}: exiting thread".format(self.name))