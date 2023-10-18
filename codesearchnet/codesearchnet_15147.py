def place_svg_use_coords(self, x, y, symbol_id, layer_id, group=None):
        """Similar to :meth:`place` but with an id as :paramref:`symbol_id`.

        :param str symbol_id: an id which identifies an svg object defined in
          the defs
        :param dict group: a dictionary of values to add to the group the
          use statement will be added to or :obj:`None` if nothing
          should be added
        """
        if group is None:
            group = {}
        use = {"@x": x, "@y": y, "@xlink:href": "#{}".format(symbol_id)}
        group_ = {"use": use}
        group_.update(group)
        layer = self._get_layer(layer_id)
        layer["g"].append(group_)