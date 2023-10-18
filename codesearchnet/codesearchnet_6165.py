def _check_lock_permission(
        self, url, lock_type, lock_scope, lock_depth, token_list, principal
    ):
        """Check, if <principal> can lock <url>, otherwise raise an error.

        If locking <url> would create a conflict, DAVError(HTTP_LOCKED) is
        raised. An embedded DAVErrorCondition contains the conflicting resource.

        @see http://www.webdav.org/specs/rfc4918.html#lock-model

        - Parent locks WILL NOT be conflicting, if they are depth-0.
        - Exclusive depth-infinity parent locks WILL be conflicting, even if
          they are owned by <principal>.
        - Child locks WILL NOT be conflicting, if we request a depth-0 lock.
        - Exclusive child locks WILL be conflicting, even if they are owned by
          <principal>. (7.7)
        - It is not enough to check whether a lock is owned by <principal>, but
          also the token must be passed with the request. (Because <principal>
          may run two different applications on his client.)
        - <principal> cannot lock-exclusive, if he holds a parent shared-lock.
          (This would only make sense, if he was the only shared-lock holder.)
        - TODO: litmus tries to acquire a shared lock on one resource twice
          (locks: 27 'double_sharedlock') and fails, when we return HTTP_LOCKED.
          So we allow multi shared locks on a resource even for the same
          principal.

        @param url: URL that shall be locked
        @param lock_type: "write"
        @param lock_scope: "shared"|"exclusive"
        @param lock_depth: "0"|"infinity"
        @param token_list: list of lock tokens, that the user submitted in If: header
        @param principal: name of the principal requesting a lock

        @return: None (or raise)
        """
        assert lock_type == "write"
        assert lock_scope in ("shared", "exclusive")
        assert lock_depth in ("0", "infinity")

        _logger.debug(
            "checkLockPermission({}, {}, {}, {})".format(
                url, lock_scope, lock_depth, principal
            )
        )

        # Error precondition to collect conflicting URLs
        errcond = DAVErrorCondition(PRECONDITION_CODE_LockConflict)

        self._lock.acquire_read()
        try:
            # Check url and all parents for conflicting locks
            u = url
            while u:
                ll = self.get_url_lock_list(u)
                for l in ll:
                    _logger.debug("    check parent {}, {}".format(u, lock_string(l)))
                    if u != url and l["depth"] != "infinity":
                        # We only consider parents with Depth: infinity
                        continue
                    elif l["scope"] == "shared" and lock_scope == "shared":
                        # Only compatible with shared locks (even by same
                        # principal)
                        continue
                    # Lock conflict
                    _logger.debug(
                        " -> DENIED due to locked parent {}".format(lock_string(l))
                    )
                    errcond.add_href(l["root"])
                u = util.get_uri_parent(u)

            if lock_depth == "infinity":
                # Check child URLs for conflicting locks
                childLocks = self.storage.get_lock_list(
                    url, include_root=False, include_children=True, token_only=False
                )

                for l in childLocks:
                    assert util.is_child_uri(url, l["root"])
                    #                    if util.is_child_uri(url, l["root"]):
                    _logger.debug(
                        " -> DENIED due to locked child {}".format(lock_string(l))
                    )
                    errcond.add_href(l["root"])
        finally:
            self._lock.release()

        # If there were conflicts, raise HTTP_LOCKED for <url>, and pass
        # conflicting resource with 'no-conflicting-lock' precondition
        if len(errcond.hrefs) > 0:
            raise DAVError(HTTP_LOCKED, err_condition=errcond)
        return