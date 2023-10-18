def market_normal(self, session, after_open, before_close) -> Session:
        """
        Time intervals between market

        Args:
            session: [allday, day, am, pm, night]
            after_open: mins after open
            before_close: mins before close

        Returns:
            Session of start_time and end_time
        """
        logger = logs.get_logger(self.market_normal)

        if session not in self.exch: return SessNA
        ss = self.exch[session]

        s_time = shift_time(ss[0], int(after_open) + 1)
        e_time = shift_time(ss[-1], -int(before_close))

        request_cross = pd.Timestamp(s_time) >= pd.Timestamp(e_time)
        session_cross = pd.Timestamp(ss[0]) >= pd.Timestamp(ss[1])
        if request_cross and (not session_cross):
            logger.warning(f'end time {e_time} is earlier than {s_time} ...')
            return SessNA

        return Session(s_time, e_time)