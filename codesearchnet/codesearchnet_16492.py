def upgrade(self):
        """Upgrade deployment."""
        if not self.is_valid:
            raise PolyaxonDeploymentConfigError(
                'Deployment type `{}` not supported'.format(self.deployment_type))

        if self.is_kubernetes:
            self.upgrade_on_kubernetes()
        elif self.is_docker_compose:
            self.upgrade_on_docker_compose()
        elif self.is_docker:
            self.upgrade_on_docker()
        elif self.is_heroku:
            self.upgrade_on_heroku()