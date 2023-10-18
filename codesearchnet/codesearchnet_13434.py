def display_name(self):
        """Get human-readable subject name derived from the SubjectName
        or SubjectAltName field.
        """
        if self.subject_name:
            return u", ".join( [ u", ".join(
                        [ u"{0}={1}".format(k,v) for k, v in dn_tuple ] )
                            for dn_tuple in self.subject_name ])
        for name_type in ("XmppAddr", "DNS", "SRV"):
            names = self.alt_names.get(name_type)
            if names:
                return names[0]
        return u"<unknown>"