def execute(self, correlation_id, args):
        """
        Executes the command given specific arguments as an input.
        
        Args:
            correlation_id: a unique correlation/transaction id
            args: command arguments
        
        Returns: an execution result.
        
        Raises:
            ApplicationException: when execution fails for whatever reason.
        """
        # Validate arguments
        if self._schema != None:
            self.validate_and_throw_exception(correlation_id, args)
        
        # Call the function
        try:
            return self._function(correlation_id, args)
        # Intercept unhandled errors
        except Exception as ex:
            raise InvocationException(
                correlation_id,
                "EXEC_FAILED",
                "Execution " + self._name + " failed: " + str(ex)
            ).with_details("command", self._name).wrap(ex)