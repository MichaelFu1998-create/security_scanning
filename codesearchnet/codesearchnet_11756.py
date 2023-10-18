def what_requires(self, name):
        """
        Lists the packages that require the given package.
        """
        r = self.local_renderer
        r.env.name = name
        r.local('pipdeptree -p {name} --reverse')