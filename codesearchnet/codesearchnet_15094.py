def to_svg(self, instruction_or_id,
               i_promise_not_to_change_the_result=False):
        """Return the SVG for an instruction.

        :param instruction_or_id: either an
          :class:`~knittingpattern.Instruction.Instruction` or an id
          returned by :meth:`get_instruction_id`
        :param bool i_promise_not_to_change_the_result:

          - :obj:`False`: the result is copied, you can alter it.
          - :obj:`True`: the result is directly from the cache. If you change
            the result, other calls of this function get the changed result.

        :return: an SVGDumper
        :rtype: knittingpattern.Dumper.SVGDumper
        """
        return self._new_svg_dumper(lambda: self.instruction_to_svg_dict(
            instruction_or_id, not i_promise_not_to_change_the_result))