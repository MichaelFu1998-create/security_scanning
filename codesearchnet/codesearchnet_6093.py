def get_descendants(
        self,
        collections=True,
        resources=True,
        depth_first=False,
        depth="infinity",
        add_self=False,
    ):
        """Return a list _DAVResource objects of a collection (children,
        grand-children, ...).

        This default implementation calls self.get_member_list() recursively.

        This function may also be called for non-collections (with add_self=True).

        :Parameters:
            depth_first : bool
                use <False>, to list containers before content.
                (e.g. when moving / copying branches.)
                Use <True>, to list content before containers.
                (e.g. when deleting branches.)
            depth : string
                '0' | '1' | 'infinity'
        """
        assert depth in ("0", "1", "infinity")
        res = []
        if add_self and not depth_first:
            res.append(self)
        if depth != "0" and self.is_collection:
            for child in self.get_member_list():
                if not child:
                    self.get_member_list()
                want = (collections and child.is_collection) or (
                    resources and not child.is_collection
                )
                if want and not depth_first:
                    res.append(child)
                if child.is_collection and depth == "infinity":
                    res.extend(
                        child.get_descendants(
                            collections, resources, depth_first, depth, add_self=False
                        )
                    )
                if want and depth_first:
                    res.append(child)
        if add_self and depth_first:
            res.append(self)
        return res