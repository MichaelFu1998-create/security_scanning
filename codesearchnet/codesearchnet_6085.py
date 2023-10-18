def handle_copy(self, dest_path, depth_infinity):
        """Handle a COPY request natively.

        """
        destType, destHgPath = util.pop_path(dest_path)
        destHgPath = destHgPath.strip("/")
        ui = self.provider.ui
        repo = self.provider.repo
        _logger.info("handle_copy %s -> %s" % (self.localHgPath, destHgPath))
        if self.rev is None and destType == "edit":
            # COPY /edit/a/b to /edit/c/d: turn into 'hg copy -f a/b c/d'
            commands.copy(ui, repo, self.localHgPath, destHgPath, force=True)
        elif self.rev is None and destType == "released":
            # COPY /edit/a/b to /released/c/d
            # This is interpreted as 'hg commit a/b' (ignoring the dest. path)
            self._commit("WsgiDAV commit (COPY %s -> %s)" % (self.path, dest_path))
        else:
            raise DAVError(HTTP_FORBIDDEN)
        # Return True: request was handled
        return True