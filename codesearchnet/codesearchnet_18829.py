def convert_all(cls, records):
        """Convert the list of bibrecs into one MARCXML.

        >>> from harvestingkit.bibrecord import BibRecordPackage
        >>> from harvestingkit.inspire_cds_package import Inspire2CDS
        >>> bibrecs = BibRecordPackage("inspire.xml")
        >>> bibrecs.parse()
        >>> xml = Inspire2CDS.convert_all(bibrecs.get_records())

        :param records: list of BibRecord dicts
        :type records: list

        :returns: MARCXML as string
        """
        out = ["<collection>"]
        for rec in records:
            conversion = cls(rec)
            out.append(conversion.convert())
        out.append("</collection>")
        return "\n".join(out)