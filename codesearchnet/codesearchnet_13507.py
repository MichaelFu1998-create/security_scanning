def set_identities(self,identities):
        """Set identities in the disco#info object.

        Remove all existing identities from `self`.

        :Parameters:
            - `identities`: list of identities or identity properties
              (jid,node,category,type,name).
        :Types:
            - `identities`: sequence of `DiscoIdentity` or sequence of sequences
        """
        for identity in self.identities:
            identity.remove()
        for identity in identities:
            try:
                self.add_identity(identity.name,identity.category,identity.type)
            except AttributeError:
                self.add_identity(*identity)