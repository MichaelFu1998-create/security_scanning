def create_vpc(self):
        """Create and configure VPC

        We create a VPC with CIDR 10.0.0.0/16, which provides up to 64,000 instances.

        We attach a subnet for each availability zone within the region specified in the
        config. We give each subnet an ip range like 10.0.X.0/20, which is large enough
        for approx. 4000 instances.

        Security groups are configured in function security_group.
        """

        try:
            # We use a large VPC so that the cluster can get large
            vpc = self.ec2.create_vpc(
                CidrBlock='10.0.0.0/16',
                AmazonProvidedIpv6CidrBlock=False,
            )
        except Exception as e:
            # This failure will cause a full abort
            logger.error("{}\n".format(e))
            raise e

        # Attach internet gateway so that our cluster can
        # talk to the outside internet
        internet_gateway = self.ec2.create_internet_gateway()
        internet_gateway.attach_to_vpc(VpcId=vpc.vpc_id)  # Returns None
        self.internet_gateway = internet_gateway.id

        # Create and configure route table to allow proper traffic
        route_table = self.config_route_table(vpc, internet_gateway)
        self.route_table = route_table.id

        # Get all avaliability zones
        availability_zones = self.client.describe_availability_zones()

        # go through AZs and set up a subnet per
        for num, zone in enumerate(availability_zones['AvailabilityZones']):
            if zone['State'] == "available":

                # Create a large subnet (4000 max nodes)
                subnet = vpc.create_subnet(
                    CidrBlock='10.0.{}.0/20'.format(16 * num), AvailabilityZone=zone['ZoneName']
                )

                # Make subnet accessible
                subnet.meta.client.modify_subnet_attribute(
                    SubnetId=subnet.id, MapPublicIpOnLaunch={"Value": True}
                )

                route_table.associate_with_subnet(SubnetId=subnet.id)
                self.sn_ids.append(subnet.id)
            else:
                logger.info("{} unavailable".format(zone['ZoneName']))
        # Security groups
        self.security_group(vpc)
        self.vpc_id = vpc.id
        return vpc