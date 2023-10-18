def config_route_table(self, vpc, internet_gateway):
        """Configure route table for Virtual Private Cloud (VPC).

        Parameters
        ----------
        vpc : dict
            Representation of the VPC (created by create_vpc()).
        internet_gateway : dict
            Representation of the internet gateway (created by create_vpc()).
        """
        route_table = vpc.create_route_table()
        route_table.create_route(
            DestinationCidrBlock='0.0.0.0/0', GatewayId=internet_gateway.internet_gateway_id
        )
        return route_table