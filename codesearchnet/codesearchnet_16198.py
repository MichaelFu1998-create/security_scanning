def execute_async_script(self, script, *args):
        """Execute JavaScript Asynchronously in current context.

        Support:
            Web(WebView)

        Args:
            script: The JavaScript to execute.
            *args: Arguments for your JavaScript.

        Returns:
            Returns the return value of the function.
        """
        return self._execute(Command.EXECUTE_ASYNC_SCRIPT, {
            'script': script,
            'args': list(args)})