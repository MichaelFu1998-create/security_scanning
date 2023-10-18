def _create_deployment(self, deployment):
        """ Create the kubernetes deployment """

        api_response = self.kube_client.create_namespaced_deployment(
            body=deployment,
            namespace=self.namespace)

        logger.debug("Deployment created. status='{0}'".format(str(api_response.status)))