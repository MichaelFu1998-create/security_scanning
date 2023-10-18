def save_statement(self, statement):
        """
        Save xAPI statement.

        Arguments:
            statement (EnterpriseStatement): xAPI Statement to send to the LRS.

        Raises:
            ClientError: If xAPI statement fails to save.
        """
        response = self.lrs.save_statement(statement)

        if not response:
            raise ClientError('EnterpriseXAPIClient request failed.')