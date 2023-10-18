def place_svg_dict(self, x, y, svg_dict, layer_id, group=None):
        """Same as :meth:`place` but with a dictionary as :paramref:`svg_dict`.

        :param dict svg_dict: a dictionary returned by `xmltodict.parse()
          <https://github.com/martinblech/xmltodict>`__
        :param dict group: a dictionary of values to add to the group the
          :paramref:`svg_dict` will be added to or :obj:`None` if nothing
          should be added
        """
        if group is None:
            group = {}
        group_ = {
            "@transform": "translate({},{})".format(x, y),
            "g": list(svg_dict.values())
        }
        group_.update(group)
        layer = self._get_layer(layer_id)
        layer["g"].append(group_)