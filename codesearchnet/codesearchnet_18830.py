def from_source(cls, source):
        """Yield single conversion objects from a MARCXML file or string.

        >>> from harvestingkit.inspire_cds_package import Inspire2CDS
        >>> for record in Inspire2CDS.from_source("inspire.xml"):
        >>>     xml = record.convert()

        """
        bibrecs = BibRecordPackage(source)
        bibrecs.parse()
        for bibrec in bibrecs.get_records():
            yield cls(bibrec)