def _create_deployment_object(self, job_name, job_image,
                                  deployment_name, port=80,
                                  replicas=1,
                                  cmd_string=None,
                                  engine_json_file='~/.ipython/profile_default/security/ipcontroller-engine.json',
                                  engine_dir='.',
                                  volumes=[]):
        """ Create a kubernetes deployment for the job.
        Args:
              - job_name (string) : Name of the job and deployment
              - job_image (string) : Docker image to launch
        KWargs:
             - port (integer) : Container port
             - replicas : Number of replica containers to maintain
        Returns:
              - True: The deployment object to launch
        """

        # sorry, quick hack that doesn't pass this stuff through to test it works.
        # TODO it also doesn't only add what is set :(
        security_context = None
        if self.user_id and self.group_id:
            security_context = client.V1SecurityContext(run_as_group=self.group_id,
                                                        run_as_user=self.user_id,
                                                        run_as_non_root=self.run_as_non_root)

        # Create the enviornment variables and command to initiate IPP
        environment_vars = client.V1EnvVar(name="TEST", value="SOME DATA")

        launch_args = ["-c", "{0}; /app/deploy.sh;".format(cmd_string)]

        volume_mounts = []
        # Create mount paths for the volumes
        for volume in volumes:
            volume_mounts.append(client.V1VolumeMount(mount_path=volume[1],
                                                      name=volume[0]))
        # Configureate Pod template container
        container = None
        if security_context:
            container = client.V1Container(
                name=job_name,
                image=job_image,
                ports=[client.V1ContainerPort(container_port=port)],
                volume_mounts=volume_mounts,
                command=['/bin/bash'],
                args=launch_args,
                env=[environment_vars],
                security_context=security_context)
        else:
            container = client.V1Container(
                name=job_name,
                image=job_image,
                ports=[client.V1ContainerPort(container_port=port)],
                volume_mounts=volume_mounts,
                command=['/bin/bash'],
                args=launch_args,
                env=[environment_vars])
        # Create a secret to enable pulling images from secure repositories
        secret = None
        if self.secret:
            secret = client.V1LocalObjectReference(name=self.secret)

        # Create list of volumes from (pvc, mount) tuples
        volume_defs = []
        for volume in volumes:
            volume_defs.append(client.V1Volume(name=volume[0],
                                               persistent_volume_claim=client.V1PersistentVolumeClaimVolumeSource(
                                                   claim_name=volume[0])))

        # Create and configurate a spec section
        template = client.V1PodTemplateSpec(
            metadata=client.V1ObjectMeta(labels={"app": job_name}),
            spec=client.V1PodSpec(containers=[container],
                                  image_pull_secrets=[secret],
                                  volumes=volume_defs
                                  ))

        # Create the specification of deployment
        spec = client.ExtensionsV1beta1DeploymentSpec(replicas=replicas,
                                                      template=template)

        # Instantiate the deployment object
        deployment = client.ExtensionsV1beta1Deployment(
            api_version="extensions/v1beta1",
            kind="Deployment",
            metadata=client.V1ObjectMeta(name=deployment_name),
            spec=spec)

        return deployment