def __intermediate_bridge(self, interface, i):
        """
        converts NetJSON bridge to
        UCI intermediate data structure
        """
        # ensure type "bridge" is only given to one logical interface
        if interface['type'] == 'bridge' and i < 2:
            bridge_members = ' '.join(interface.pop('bridge_members'))
            # put bridge members in ifname attribute
            if bridge_members:
                interface['ifname'] = bridge_members
            # if no members, this is an empty bridge
            else:
                interface['bridge_empty'] = True
                del interface['ifname']
        # bridge has already been defined
        # but we need to add more references to it
        elif interface['type'] == 'bridge' and i >= 2:
            # openwrt adds "br-" prefix to bridge interfaces
            # we need to take this into account when referring
            # to these physical names
            if 'br-' not in interface['ifname']:
                interface['ifname'] = 'br-{ifname}'.format(**interface)
            # do not repeat bridge attributes (they have already been processed)
            for attr in ['type', 'bridge_members', 'stp', 'gateway']:
                if attr in interface:
                    del interface[attr]
        elif interface['type'] != 'bridge':
            del interface['type']
        return interface