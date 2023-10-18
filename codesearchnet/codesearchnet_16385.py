async def load_project(self, project_path):
        """Load a project.

        :param project_path: Path to project you want to load.
        """
        cmd = "loadproject %s" % project_path
        return await asyncio.wait_for(
            self._protocol.send_command(cmd), timeout=self._timeout
        )