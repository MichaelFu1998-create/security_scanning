def get_siblings(self, objectId, subreference, passage):
        """ Get siblings of a browsed subreference

        .. note:: Since 1.0.0c, there is no more prevnext dict. Nemo uses the list of original\
        chunked references to retrieve next and previous, or simply relies on the resolver to get siblings\
        when the subreference is not found in given original chunks.

        :param objectId: Id of the object
        :param subreference: Subreference of the object
        :param passage: Current Passage
        :return: Previous and next references
        :rtype: (str, str)
        """
        reffs = [reff for reff, _ in self.get_reffs(objectId)]
        if subreference in reffs:
            index = reffs.index(subreference)
            # Not the first item and not the last one
            if 0 < index < len(reffs) - 1:
                return reffs[index-1], reffs[index+1]
            elif index == 0 and index < len(reffs) - 1:
                return None, reffs[1]
            elif index > 0 and index == len(reffs) - 1:
                return reffs[index-1], None
            else:
                return None, None
        else:
            return passage.siblingsId