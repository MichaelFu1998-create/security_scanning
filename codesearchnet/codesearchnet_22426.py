def close(self):
        """Close the http/https connect."""
        try:
            self.response.close()
            self.logger.debug("close connect succeed.")
        except Exception as e:
            self.unknown("close connect error: %s" % e)