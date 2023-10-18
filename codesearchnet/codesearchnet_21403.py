def get_users(self, *args, **kwargs):
        """
            Retrieves the users from elastic.
        """
        arguments, _ = self.argparser.parse_known_args()
        if self.is_pipe and self.use_pipe:
            return self.get_pipe(self.object_type)
        elif arguments.tags or arguments.group or arguments.search or arguments.domain:
            return self.argument_search()
        else:
            return self.search(*args, **kwargs)