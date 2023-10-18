def spin_up_instance(self, command, job_name):
        """Start an instance in the VPC in the first available subnet.

        N instances will be started if nodes_per_block > 1.
        Not supported. We only do 1 node per block.

        Parameters
        ----------
        command : str
            Command string to execute on the node.
        job_name : str
            Name associated with the instances.
        """

        command = Template(template_string).substitute(jobname=job_name,
                                                       user_script=command,
                                                       linger=str(self.linger).lower(),
                                                       worker_init=self.worker_init)
        instance_type = self.instance_type
        subnet = self.sn_ids[0]
        ami_id = self.image_id
        total_instances = len(self.instances)

        if float(self.spot_max_bid) > 0:
            spot_options = {
                'MarketType': 'spot',
                'SpotOptions': {
                    'MaxPrice': str(self.spot_max_bid),
                    'SpotInstanceType': 'one-time',
                    'InstanceInterruptionBehavior': 'terminate'
                }
            }
        else:
            spot_options = {}

        if total_instances > self.max_nodes:
            logger.warn("Exceeded instance limit ({}). Cannot continue\n".format(self.max_nodes))
            return [None]
        try:
            tag_spec = [{"ResourceType": "instance", "Tags": [{'Key': 'Name', 'Value': job_name}]}]

            instance = self.ec2.create_instances(
                MinCount=1,
                MaxCount=1,
                InstanceType=instance_type,
                ImageId=ami_id,
                KeyName=self.key_name,
                SubnetId=subnet,
                SecurityGroupIds=[self.sg_id],
                TagSpecifications=tag_spec,
                InstanceMarketOptions=spot_options,
                InstanceInitiatedShutdownBehavior='terminate',
                IamInstanceProfile={'Arn': self.iam_instance_profile_arn},
                UserData=command
            )
        except ClientError as e:
            print(e)
            logger.error(e.response)
            return [None]

        except Exception as e:
            logger.error("Request for EC2 resources failed : {0}".format(e))
            return [None]

        self.instances.append(instance[0].id)
        logger.info(
            "Started up 1 instance {} . Instance type:{}".format(instance[0].id, instance_type)
        )
        return instance