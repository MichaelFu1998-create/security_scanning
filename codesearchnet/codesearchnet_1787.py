def getaddrlist(self, name):
        """Get a list of addresses from a header.

        Retrieves a list of addresses from a header, where each address is a
        tuple as returned by getaddr().  Scans all named headers, so it works
        properly with multiple To: or Cc: headers for example.
        """
        raw = []
        for h in self.getallmatchingheaders(name):
            if h[0] in ' \t':
                raw.append(h)
            else:
                if raw:
                    raw.append(', ')
                i = h.find(':')
                if i > 0:
                    addr = h[i+1:]
                raw.append(addr)
        alladdrs = ''.join(raw)
        a = AddressList(alladdrs)
        return a.addresslist