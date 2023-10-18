def build_tool(self, doc, entity):
        """Builds a tool object out of a string representation.
        Returns built tool. Raises SPDXValueError if failed to extract
        tool name or name is malformed
        """
        match = self.tool_re.match(entity)
        if match and validations.validate_tool_name(match.group(self.TOOL_NAME_GROUP)):
            name = match.group(self.TOOL_NAME_GROUP)
            return creationinfo.Tool(name)
        else:
            raise SPDXValueError('Failed to extract tool name')