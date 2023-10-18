def get_resource_inst(self, path, environ):
        """Return HgResource object for path.

        See DAVProvider.get_resource_inst()
        """
        self._count_get_resource_inst += 1

        # HG expects the resource paths without leading '/'
        localHgPath = path.strip("/")
        rev = None
        cmd, rest = util.pop_path(path)

        if cmd == "":
            return VirtualCollection(
                path, environ, "root", ["edit", "released", "archive"]
            )
        elif cmd == "edit":
            localHgPath = rest.strip("/")
            rev = None
        elif cmd == "released":
            localHgPath = rest.strip("/")
            rev = "tip"
        elif cmd == "archive":
            if rest == "/":
                # Browse /archive: return a list of revision folders:
                loglist = self._get_log(limit=10)
                members = [compat.to_native(l["local_id"]) for l in loglist]
                return VirtualCollection(path, environ, "Revisions", members)
            revid, rest = util.pop_path(rest)
            try:
                int(revid)
            except Exception:
                # Tried to access /archive/anyname
                return None
            # Access /archive/19
            rev = revid
            localHgPath = rest.strip("/")
        else:
            return None

        # read mercurial repo into request cache
        cache = self._get_repo_info(environ, rev)

        if localHgPath in cache["filedict"]:
            # It is a version controlled file
            return HgResource(path, False, environ, rev, localHgPath)

        if localHgPath in cache["dirinfos"] or localHgPath == "":
            # It is an existing folder
            return HgResource(path, True, environ, rev, localHgPath)
        return None