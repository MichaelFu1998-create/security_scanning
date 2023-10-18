def create(self, type, name=None, data=None, priority=None,
               port=None, weight=None):
        """
        Parameters
        ----------
        type: str
            {A, AAAA, CNAME, MX, TXT, SRV, NS}
        name: str
            Name of the record
        data: object, type-dependent
            type == 'A' : IPv4 address
            type == 'AAAA' : IPv6 address
            type == 'CNAME' : destination host name
            type == 'MX' : mail host name
            type == 'TXT' : txt contents
            type == 'SRV' : target host name to direct requests for the service
            type == 'NS' :  name server that is authoritative for the domain
        priority:
        port:
        weight:
        """
        if type == 'A' and name is None:
            name = self.domain
        return self.post(type=type, name=name, data=data, priority=priority,
                         port=port, weight=weight)[self.singular]