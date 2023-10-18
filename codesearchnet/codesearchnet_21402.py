def id_to_object(self, line):
        """
            Resolves the given id to a user object, if it doesn't exists it will be created.
        """
        user = User.get(line, ignore=404)
        if not user:
            user = User(username=line)
            user.save()
        return user