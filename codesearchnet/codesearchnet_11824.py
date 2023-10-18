def record_manifest(self):
        """
        Returns a dictionary representing a serialized state of the service.
        """
        data = {}
        data['required_packages'] = self.install_required(type=SYSTEM, verbose=False, list_only=True)
        data['required_packages'].sort()
        data['custom_packages'] = self.install_custom(list_only=True)
        data['custom_packages'].sort()
        data['repositories'] = self.get_repositories()
        return data