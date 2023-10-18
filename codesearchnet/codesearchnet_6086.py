def _get_log(self, limit=None):
        """Read log entries into a list of dictionaries."""
        self.ui.pushbuffer()
        commands.log(self.ui, self.repo, limit=limit, date=None, rev=None, user=None)
        res = self.ui.popbuffer().strip()

        logList = []
        for logentry in res.split("\n\n"):
            log = {}
            logList.append(log)
            for line in logentry.split("\n"):
                k, v = line.split(":", 1)
                assert k in ("changeset", "tag", "user", "date", "summary")
                log[k.strip()] = v.strip()
            log["parsed_date"] = util.parse_time_string(log["date"])
            local_id, unid = log["changeset"].split(":")
            log["local_id"] = int(local_id)
            log["unid"] = unid
        #        pprint(logList)
        return logList