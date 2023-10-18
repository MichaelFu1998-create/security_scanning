def update_group_states_for_vifs(self, vifs, ack):
        """Updates security groups by setting the ack field"""
        vif_keys = [self.vif_key(vif.device_id, vif.mac_address)
                    for vif in vifs]
        self.set_fields(vif_keys, SECURITY_GROUP_ACK, ack)