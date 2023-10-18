def build_SVG_dict(self):
        """Go through the layout and build the SVG.

        :return: an xml dict that can be exported using a
          :class:`~knittingpattern.Dumper.XMLDumper`
        :rtype: dict
        """
        zoom = self._zoom
        layout = self._layout
        builder = self._builder
        bbox = list(map(lambda f: f * zoom, layout.bounding_box))
        builder.bounding_box = bbox
        flip_x = bbox[2] + bbox[0] * 2
        flip_y = bbox[3] + bbox[1] * 2
        instructions = list(layout.walk_instructions(
            lambda i: (flip_x - (i.x + i.width) * zoom,
                       flip_y - (i.y + i.height) * zoom,
                       i.instruction)))
        instructions.sort(key=lambda x_y_i: x_y_i[2].render_z)
        for x, y, instruction in instructions:
            render_z = instruction.render_z
            z_id = ("" if not render_z else "-{}".format(render_z))
            layer_id = "row-{}{}".format(instruction.row.id, z_id)
            def_id = self._register_instruction_in_defs(instruction)
            scale = self._symbol_id_to_scale[def_id]
            group = {
                "@class": "instruction",
                "@id": "instruction-{}".format(instruction.id),
                "@transform": "translate({},{}),scale({})".format(
                    x, y, scale)
            }
            builder.place_svg_use(def_id, layer_id, group)
        builder.insert_defs(self._instruction_type_color_to_symbol.values())
        return builder.get_svg_dict()