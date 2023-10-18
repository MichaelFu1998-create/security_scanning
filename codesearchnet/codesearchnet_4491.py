def security_group(self, vpc):
        """Create and configure a new security group.

        Allows all ICMP in, all TCP and UDP in within VPC.

        This security group is very open. It allows all incoming ping requests on all
        ports. It also allows all outgoing traffic on all ports. This can be limited by
        changing the allowed port ranges.

        Parameters
        ----------
        vpc : VPC instance
            VPC in which to set up security group.
        """

        sg = vpc.create_security_group(
            GroupName="private-subnet", Description="security group for remote executors"
        )

        ip_ranges = [{'CidrIp': '10.0.0.0/16'}]

        # Allows all ICMP in, all TCP and UDP in within VPC
        in_permissions = [
            {
                'IpProtocol': 'TCP',
                'FromPort': 0,
                'ToPort': 65535,
                'IpRanges': ip_ranges,
            }, {
                'IpProtocol': 'UDP',
                'FromPort': 0,
                'ToPort': 65535,
                'IpRanges': ip_ranges,
            }, {
                'IpProtocol': 'ICMP',
                'FromPort': -1,
                'ToPort': -1,
                'IpRanges': [{
                    'CidrIp': '0.0.0.0/0'
                }],
            }, {
                'IpProtocol': 'TCP',
                'FromPort': 22,
                'ToPort': 22,
                'IpRanges': [{
                    'CidrIp': '0.0.0.0/0'
                }],
            }
        ]

        # Allows all TCP out, all TCP and UDP out within VPC
        out_permissions = [
            {
                'IpProtocol': 'TCP',
                'FromPort': 0,
                'ToPort': 65535,
                'IpRanges': [{
                    'CidrIp': '0.0.0.0/0'
                }],
            },
            {
                'IpProtocol': 'TCP',
                'FromPort': 0,
                'ToPort': 65535,
                'IpRanges': ip_ranges,
            },
            {
                'IpProtocol': 'UDP',
                'FromPort': 0,
                'ToPort': 65535,
                'IpRanges': ip_ranges,
            },
        ]

        sg.authorize_ingress(IpPermissions=in_permissions)
        sg.authorize_egress(IpPermissions=out_permissions)
        self.sg_id = sg.id
        return sg