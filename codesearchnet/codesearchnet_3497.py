def awake(self, procid):
        """ Remove procid from waitlists and reestablish it in the running list """
        logger.debug(f"Remove procid:{procid} from waitlists and reestablish it in the running list")
        for wait_list in self.rwait:
            if procid in wait_list:
                wait_list.remove(procid)
        for wait_list in self.twait:
            if procid in wait_list:
                wait_list.remove(procid)
        self.timers[procid] = None
        self.running.append(procid)
        if self._current is None:
            self._current = procid