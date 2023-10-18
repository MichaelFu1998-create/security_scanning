def set_fixed_capabils(self, capabils):
        """set keys of capabils into fields of object
        :capabils: dict
        """
        self.ess = capabils['ess']
        self.ibss = capabils['ibss']
        self.priv = capabils['priv']
        self.short_preamble = capabils['short_preamble']
        self.pbcc = capabils['pbcc']
        self.chan_agility = capabils['chan_agility']
        self.spec_man = capabils['spec_man']
        self.short_slot = capabils['short_slot']
        self.apsd = capabils['apsd']
        self.radio_meas = capabils['radio_meas']
        self.dss_ofdm = capabils['dss_ofdm']
        self.del_back = capabils['del_back']
        self.imm_back = capabils['imm_back']