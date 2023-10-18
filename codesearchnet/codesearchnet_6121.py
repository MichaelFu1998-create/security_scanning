def _check_write_permission(self, res, depth, environ):
        """Raise DAVError(HTTP_LOCKED), if res is locked.

        If depth=='infinity', we also raise when child resources are locked.
        """
        lockMan = self._davProvider.lock_manager
        if lockMan is None or res is None:
            return True

        refUrl = res.get_ref_url()

        if "wsgidav.conditions.if" not in environ:
            util.parse_if_header_dict(environ)

        # raise HTTP_LOCKED if conflict exists
        lockMan.check_write_permission(
            refUrl,
            depth,
            environ["wsgidav.ifLockTokenList"],
            environ["wsgidav.user_name"],
        )