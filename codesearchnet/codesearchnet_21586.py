def _file_path(self, uid):
        """Create and return full file path for DayOne entry"""
        file_name = '%s.doentry' % (uid)
        return os.path.join(self.dayone_journal_path, file_name)