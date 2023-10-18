def get_effect_resources(self) -> List[Any]:
        """
        Get all resources registed in effect packages.
        These are typically located in ``resources.py``
        """
        resources = []
        for package in self.packages:
            resources.extend(package.resources)

        return resources