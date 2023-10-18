def close(self):
    """Deletes temporary system objects/files. """
    if self._tempDir is not None and os.path.isdir(self._tempDir):
      self.logger.debug("Removing temporary directory %r", self._tempDir)
      shutil.rmtree(self._tempDir)
      self._tempDir = None

    return