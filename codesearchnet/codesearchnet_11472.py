def on_tool_finish(self, tool):
        """
        Called when an individual tool completes execution.

        :param tool: the name of the tool that completed
        :type tool: str
        """

        with self._lock:
            if tool in self.current_tools:
                self.current_tools.remove(tool)
                self.completed_tools.append(tool)