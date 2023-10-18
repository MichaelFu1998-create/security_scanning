def _delete_deployment(self, deployment_name):
        """ Delete deployment """

        api_response = self.kube_client.delete_namespaced_deployment(
            name=deployment_name,
            namespace=self.namespace,
            body=client.V1DeleteOptions(
                propagation_policy='Foreground',
                grace_period_seconds=5))

        logger.debug("Deployment deleted. status='{0}'".format(
            str(api_response.status)))