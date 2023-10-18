def market_exact(self, session, start_time: str, end_time: str) -> Session:
        """
        Explicitly specify start time and end time

        Args:
            session: predefined session
            start_time: start time in terms of HHMM string
            end_time: end time in terms of HHMM string

        Returns:
            Session of start_time and end_time
        """
        if session not in self.exch: return SessNA
        ss = self.exch[session]

        same_day = ss[0] < ss[-1]

        if not start_time: s_time = ss[0]
        else:
            s_time = param.to_hour(start_time)
            if same_day: s_time = max(s_time, ss[0])

        if not end_time: e_time = ss[-1]
        else:
            e_time = param.to_hour(end_time)
            if same_day: e_time = min(e_time, ss[-1])

        if same_day and (s_time > e_time): return SessNA
        return Session(start_time=s_time, end_time=e_time)