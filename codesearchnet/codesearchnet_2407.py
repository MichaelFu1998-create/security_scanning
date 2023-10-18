def Exists(self, maxSearchSeconds: float = 5, searchIntervalSeconds: float = SEARCH_INTERVAL, printIfNotExist: bool = False) -> bool:
        """
        maxSearchSeconds: float
        searchIntervalSeconds: float
        Find control every searchIntervalSeconds seconds in maxSearchSeconds seconds.
        Return bool, True if find
        """
        if self._element and self._elementDirectAssign:
            #if element is directly assigned, not by searching, just check whether self._element is valid
            #but I can't find an API in UIAutomation that can directly check
            rootElement = GetRootControl().Element
            if self._element == rootElement:
                return True
            else:
                parentElement = _AutomationClient.instance().ViewWalker.GetParentElement(self._element)
                if parentElement:
                    return True
                else:
                    return False
        #find the element
        if len(self.searchProperties) == 0:
            raise LookupError("control's searchProperties must not be empty!")
        self._element = None
        startTime = ProcessTime()
        # Use same timeout(s) parameters for resolve all parents
        prev =  self.searchFromControl
        if prev and not prev._element and not prev.Exists(maxSearchSeconds, searchIntervalSeconds):
            if printIfNotExist or DEBUG_EXIST_DISAPPEAR:
                Logger.ColorfullyWriteLine(self.GetColorfulSearchPropertiesStr() + '<Color=Red> does not exist.</Color>')
            return False
        startTime2 = ProcessTime()
        if DEBUG_SEARCH_TIME:
            startDateTime = datetime.datetime.now()
        while True:
            control = FindControl(self.searchFromControl, self._CompareFunction, self.searchDepth, False, self.foundIndex)
            if control:
                self._element = control.Element
                control._element = 0  # control will be destroyed, but the element needs to be stroed in self._element
                if DEBUG_SEARCH_TIME:
                    Logger.ColorfullyWriteLine('{} TraverseControls: <Color=Cyan>{}</Color>, SearchTime: <Color=Cyan>{:.3f}</Color>s[{} - {}]'.format(
                        self.GetColorfulSearchPropertiesStr(), control.traverseCount, ProcessTime() - startTime2,
                        startDateTime.time(), datetime.datetime.now().time()))
                return True
            else:
                remain = startTime + maxSearchSeconds - ProcessTime()
                if remain > 0:
                    time.sleep(min(remain, searchIntervalSeconds))
                else:
                    if printIfNotExist or DEBUG_EXIST_DISAPPEAR:
                        Logger.ColorfullyWriteLine(self.GetColorfulSearchPropertiesStr() + '<Color=Red> does not exist.</Color>')
                    return False