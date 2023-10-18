def quit(self):
        """Close and exit the connection."""
        try:
            self.ftp.quit()
            self.logger.debug("quit connect succeed.")
        except ftplib.Error as e:
            self.unknown("quit connect error: %s" % e)