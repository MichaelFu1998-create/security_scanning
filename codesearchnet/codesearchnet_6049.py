def _init(self):
        """Read resource information into self._cache, for cached access.

        See DAVResource._init()
        """
        # TODO: recalc self.path from <self._file_path>, to fix correct file system case
        #       On windows this would lead to correct URLs
        self.provider._count_get_resource_inst_init += 1
        tableName, primKey = self.provider._split_path(self.path)

        display_type = "Unknown"
        displayTypeComment = ""
        contentType = "text/html"

        #        _logger.debug("getInfoDict(%s), nc=%s" % (path, self.connectCount))
        if tableName is None:
            display_type = "Database"
        elif primKey is None:  # "database" and table name
            display_type = "Database Table"
        else:
            contentType = "text/csv"
            if primKey == "_ENTIRE_CONTENTS":
                display_type = "Database Table Contents"
                displayTypeComment = "CSV Representation of Table Contents"
            else:
                display_type = "Database Record"
                displayTypeComment = "Attributes available as properties"

        # Avoid calling is_collection, since it would call isExisting -> _init_connection
        is_collection = primKey is None

        self._cache = {
            "content_length": None,
            "contentType": contentType,
            "created": time.time(),
            "display_name": self.name,
            "etag": hashlib.md5().update(self.path).hexdigest(),
            # "etag": md5.new(self.path).hexdigest(),
            "modified": None,
            "support_ranges": False,
            "display_info": {"type": display_type, "typeComment": displayTypeComment},
        }

        # Some resource-only infos:
        if not is_collection:
            self._cache["modified"] = time.time()
        _logger.debug("---> _init, nc=%s" % self.provider._count_initConnection)