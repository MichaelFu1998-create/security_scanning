def Disappears(self, maxSearchSeconds: float = 5, searchIntervalSeconds: float = SEARCH_INTERVAL, printIfNotDisappear: bool = False) -> bool:
        """
        maxSearchSeconds: float
        searchIntervalSeconds: float
        Check if control disappears every searchIntervalSeconds seconds in maxSearchSeconds seconds.
        Return bool, True if control disappears.
        """
        global DEBUG_EXIST_DISAPPEAR
        start = ProcessTime()
        while True:
            temp = DEBUG_EXIST_DISAPPEAR
            DEBUG_EXIST_DISAPPEAR = False  # do not print for Exists
            if not self.Exists(0, 0, False):
                DEBUG_EXIST_DISAPPEAR = temp
                return True
            DEBUG_EXIST_DISAPPEAR = temp
            remain = start + maxSearchSeconds - ProcessTime()
            if remain > 0:
                time.sleep(min(remain, searchIntervalSeconds))
            else:
                if printIfNotDisappear or DEBUG_EXIST_DISAPPEAR:
                    Logger.ColorfullyWriteLine(self.GetColorfulSearchPropertiesStr() + '<Color=Red> does not disappear.</Color>')
                return False