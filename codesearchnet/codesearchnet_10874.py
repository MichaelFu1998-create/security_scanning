def is_already_running(self):
        """Return True if lock exists and has not timed out."""
        date_done = (self.restore_group(self.task_identifier) or dict()).get('date_done')
        if not date_done:
            return False
        difference = datetime.utcnow() - date_done
        return difference < timedelta(seconds=self.timeout)