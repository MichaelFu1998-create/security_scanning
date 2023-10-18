def output(self, msg, newline=True):
        """
        Writes the specified string to the output target of the report.

        :param msg: the message to output.
        :type msg: str
        :param newline:
            whether or not to append a newline to the end of the message
        :type newline: str
        """

        click.echo(text_type(msg), nl=newline, file=self.output_file)