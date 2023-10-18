def set_last_modified(self, dest_path, time_stamp, dry_run):
        """Set last modified time for destPath to timeStamp on epoch-format"""
        # Translate time from RFC 1123 to seconds since epoch format
        secs = util.parse_time_string(time_stamp)
        if not dry_run:
            os.utime(self._file_path, (secs, secs))
        return True