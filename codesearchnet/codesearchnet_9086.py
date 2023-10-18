def market_close(self, session, mins) -> Session:
        """
        Time intervals for market close

        Args:
            session: [allday, day, am, pm, night]
            mins: mintues before close

        Returns:
            Session of start_time and end_time
        """
        if session not in self.exch: return SessNA
        end_time = self.exch[session][-1]
        return Session(shift_time(end_time, -int(mins) + 1), end_time)