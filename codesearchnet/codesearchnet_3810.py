def list_resource_commands(self):
        """Returns a list of multi-commands for each resource type.
        """
        resource_path = os.path.abspath(os.path.join(
            os.path.dirname(__file__),
            os.pardir,
            'resources'
        ))
        answer = set([])
        for _, name, _ in pkgutil.iter_modules([resource_path]):
            res = tower_cli.get_resource(name)
            if not getattr(res, 'internal', False):
                answer.add(name)
        return sorted(answer)