def market_open(self, session, mins) -> Session:
        """
        Time intervals for market open

        Args:
            session: [allday, day, am, pm, night]
            mins: mintues after open

        Returns:
            Session of start_time and end_time
        """
        if session not in self.exch: return SessNA
        start_time = self.exch[session][0]
        return Session(start_time, shift_time(start_time, int(mins)))