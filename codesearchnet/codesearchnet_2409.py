def Refind(self, maxSearchSeconds: float = TIME_OUT_SECOND, searchIntervalSeconds: float = SEARCH_INTERVAL, raiseException: bool = True) -> bool:
        """
        Refind the control every searchIntervalSeconds seconds in maxSearchSeconds seconds.
        maxSearchSeconds: float.
        searchIntervalSeconds: float.
        raiseException: bool, if True, raise a LookupError if timeout.
        Return bool, True if find.
        """
        if not self.Exists(maxSearchSeconds, searchIntervalSeconds, False if raiseException else DEBUG_EXIST_DISAPPEAR):
            if raiseException:
                Logger.ColorfullyWriteLine('<Color=Red>Find Control Timeout: </Color>' + self.GetColorfulSearchPropertiesStr())
                raise LookupError('Find Control Timeout: ' + self.GetSearchPropertiesStr())
            else:
                return False
        return True