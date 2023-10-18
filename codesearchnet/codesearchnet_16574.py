def get_bgp_neighbors(self):
        def generate_vrf_query(vrf_name):
            """
            Helper to provide XML-query for the VRF-type we're interested in.
            """
            if vrf_name == "global":
                rpc_command = '<Get><Operational><BGP><InstanceTable><Instance><Naming>\
                <InstanceName>default</InstanceName></Naming><InstanceActive><DefaultVRF>\
                <GlobalProcessInfo></GlobalProcessInfo><NeighborTable></NeighborTable></DefaultVRF>\
                </InstanceActive></Instance></InstanceTable></BGP></Operational></Get>'

            else:
                rpc_command = '<Get><Operational><BGP><InstanceTable><Instance><Naming>\
                <InstanceName>default</InstanceName></Naming><InstanceActive><VRFTable><VRF>\
                <Naming>{vrf_name}</Naming><GlobalProcessInfo></GlobalProcessInfo><NeighborTable>\
                </NeighborTable></VRF></VRFTable></InstanceActive></Instance></InstanceTable>\
                </BGP></Operational></Get>'.format(vrf_name=vrf_name)
            return rpc_command

        """
        Initial run to figure out what VRF's are available
        Decided to get this one from Configured-section
        because bulk-getting all instance-data to do the same could get ridiculously heavy
        Assuming we're always interested in the DefaultVRF
        """

        active_vrfs = ["global"]

        rpc_command = '<Get><Operational><BGP><ConfigInstanceTable><ConfigInstance><Naming>\
        <InstanceName>default</InstanceName></Naming><ConfigInstanceVRFTable>\
        </ConfigInstanceVRFTable></ConfigInstance></ConfigInstanceTable></BGP></Operational></Get>'

        result_tree = ETREE.fromstring(self.device.make_rpc_call(rpc_command))

        for node in result_tree.xpath('.//ConfigVRF'):
            active_vrfs.append(napalm_base.helpers.find_txt(node, 'Naming/VRFName'))

        result = {}

        for vrf in active_vrfs:
            rpc_command = generate_vrf_query(vrf)
            result_tree = ETREE.fromstring(self.device.make_rpc_call(rpc_command))

            this_vrf = {}
            this_vrf['peers'] = {}

            if vrf == "global":
                this_vrf['router_id'] = napalm_base.helpers.convert(
                    text_type, napalm_base.helpers.find_txt(result_tree,
                        'Get/Operational/BGP/InstanceTable/Instance/InstanceActive/DefaultVRF\
                        /GlobalProcessInfo/VRF/RouterID'))
            else:
                this_vrf['router_id'] = napalm_base.helpers.convert(
                    text_type, napalm_base.helpers.find_txt(result_tree,
                        'Get/Operational/BGP/InstanceTable/Instance/InstanceActive/VRFTable/VRF\
                        /GlobalProcessInfo/VRF/RouterID'))

            neighbors = {}

            for neighbor in result_tree.xpath('.//Neighbor'):
                this_neighbor = {}
                this_neighbor['local_as'] = napalm_base.helpers.convert(
                    int, napalm_base.helpers.find_txt(neighbor, 'LocalAS'))
                this_neighbor['remote_as'] = napalm_base.helpers.convert(
                    int, napalm_base.helpers.find_txt(neighbor, 'RemoteAS'))
                this_neighbor['remote_id'] = napalm_base.helpers.convert(
                    text_type, napalm_base.helpers.find_txt(neighbor, 'RouterID'))

                if napalm_base.helpers.find_txt(neighbor, 'ConnectionAdminStatus') is "1":
                    this_neighbor['is_enabled'] = True
                try:
                    this_neighbor['description'] = napalm_base.helpers.convert(
                        text_type, napalm_base.helpers.find_txt(neighbor, 'Description'))
                except AttributeError:
                    this_neighbor['description'] = u''

                this_neighbor['is_enabled'] = (
                    napalm_base.helpers.find_txt(neighbor, 'ConnectionAdminStatus') == "1")

                if str(napalm_base.helpers.find_txt(neighbor, 'ConnectionAdminStatus')) is "1":
                    this_neighbor['is_enabled'] = True
                else:
                    this_neighbor['is_enabled'] = False

                if str(napalm_base.helpers.find_txt(neighbor, 'ConnectionState')) == "BGP_ST_ESTAB":
                    this_neighbor['is_up'] = True
                    this_neighbor['uptime'] = napalm_base.helpers.convert(
                        int, napalm_base.helpers.find_txt(neighbor, 'ConnectionEstablishedTime'))
                else:
                    this_neighbor['is_up'] = False
                    this_neighbor['uptime'] = -1

                this_neighbor['address_family'] = {}

                if napalm_base.helpers.find_txt(neighbor,
                'ConnectionRemoteAddress/AFI') == "IPv4":
                    this_afi = "ipv4"
                elif napalm_base.helpers.find_txt(neighbor,
                'ConnectionRemoteAddress/AFI') == "IPv6":
                    this_afi = "ipv6"
                else:
                    this_afi = napalm_base.helpers.find_txt(neighbor, 'ConnectionRemoteAddress/AFI')

                this_neighbor['address_family'][this_afi] = {}

                try:
                    this_neighbor['address_family'][this_afi]["received_prefixes"] = \
                        napalm_base.helpers.convert(int,
                            napalm_base.helpers.find_txt(
                                neighbor, 'AFData/Entry/PrefixesAccepted'), 0) + \
                        napalm_base.helpers.convert(int,
                            napalm_base.helpers.find_txt(
                                neighbor, 'AFData/Entry/PrefixesDenied'), 0)
                    this_neighbor['address_family'][this_afi]["accepted_prefixes"] = \
                        napalm_base.helpers.convert(int,
                            napalm_base.helpers.find_txt(
                                neighbor, 'AFData/Entry/PrefixesAccepted'), 0)
                    this_neighbor['address_family'][this_afi]["sent_prefixes"] = \
                        napalm_base.helpers.convert(int,
                            napalm_base.helpers.find_txt(
                                neighbor, 'AFData/Entry/PrefixesAdvertised'), 0)
                except AttributeError:
                    this_neighbor['address_family'][this_afi]["received_prefixes"] = -1
                    this_neighbor['address_family'][this_afi]["accepted_prefixes"] = -1
                    this_neighbor['address_family'][this_afi]["sent_prefixes"] = -1

                neighbor_ip = napalm_base.helpers.ip(
                    napalm_base.helpers.find_txt(
                        neighbor, 'Naming/NeighborAddress/IPV4Address') or
                    napalm_base.helpers.find_txt(
                        neighbor, 'Naming/NeighborAddress/IPV6Address')
                )

                neighbors[neighbor_ip] = this_neighbor

            this_vrf['peers'] = neighbors
            result[vrf] = this_vrf

        return result