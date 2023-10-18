def place_svg_use(self, symbol_id, layer_id, group=None):
        """Same as :meth:`place_svg_use_coords`.

        With implicit `x`  and `y` which are set to `0` in this method and then
        :meth:`place_svg_use_coords` is called.
        """
        self.place_svg_use_coords(0, 0, symbol_id, layer_id, group)