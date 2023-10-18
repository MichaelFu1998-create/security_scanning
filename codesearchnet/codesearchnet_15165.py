def walk_connections(self, mapping=identity):
        """Iterate over connections between instructions.

        :return: an iterator over :class:`connections <Connection>` between
          :class:`instructions in grid <InstructionInGrid>`
        :param mapping: funcion to map the result, see
          :meth:`walk_instructions` for an example usage
        """
        for start in self.walk_instructions():
            for stop_instruction in start.instruction.consuming_instructions:
                if stop_instruction is None:
                    continue
                stop = self._walk.instruction_in_grid(stop_instruction)
                connection = Connection(start, stop)
                if connection.is_visible():
                    # print("connection:",
                    #      connection.start.instruction,
                    #      connection.stop.instruction)
                    yield mapping(connection)