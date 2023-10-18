def _compute_scale(self, instruction_id, svg_dict):
        """Compute the scale of an instruction svg.

        Compute the scale using the bounding box stored in the
        :paramref:`svg_dict`. The scale is saved in a dictionary using
        :paramref:`instruction_id` as key.

        :param str instruction_id: id identifying a symbol in the defs
        :param dict svg_dict: dictionary containing the SVG for the
          instruction currently processed
        """
        bbox = list(map(float, svg_dict["svg"]["@viewBox"].split()))
        scale = self._zoom / (bbox[3] - bbox[1])
        self._symbol_id_to_scale[instruction_id] = scale