def teardown(self):
        """Teardown the EC2 infastructure.

        Terminate all EC2 instances, delete all subnets, delete security group, delete VPC,
        and reset all instance variables.
        """

        self.shut_down_instance(self.instances)
        self.instances = []
        try:
            self.client.delete_internet_gateway(InternetGatewayId=self.internet_gateway)
            self.internet_gateway = None
            self.client.delete_route_table(RouteTableId=self.route_table)
            self.route_table = None
            for subnet in list(self.sn_ids):
                # Cast to list ensures that this is a copy
                # Which is important because it means that
                # the length of the list won't change during iteration
                self.client.delete_subnet(SubnetId=subnet)
                self.sn_ids.remove(subnet)
            self.client.delete_security_group(GroupId=self.sg_id)
            self.sg_id = None
            self.client.delete_vpc(VpcId=self.vpc_id)
            self.vpc_id = None
        except Exception as e:
            logger.error("{}".format(e))
            raise e
        self.show_summary()
        os.remove(self.config['state_file_path'])