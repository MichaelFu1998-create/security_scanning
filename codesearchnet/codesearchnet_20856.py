def get_pub_type(self):
        """
        Returns:
            PublicationType: :class:`.PublicationType` enum **value**.
        """
        INFO_CHAR_INDEX = 6
        SECOND_INFO_CHAR_I = 18

        if not len(self.leader) >= INFO_CHAR_INDEX + 1:
            return PublicationType.monographic

        if self.controlfields.get("FMT") == "SE":
            return PublicationType.continuing

        info_char = self.leader[INFO_CHAR_INDEX]
        multipart_n = self.get_subfields("245", "n", exception=False)
        multipart_p = self.get_subfields("245", "p", exception=False)

        if info_char in "acd":
            return PublicationType.monographic
        elif info_char in "bis":
            return PublicationType.continuing
        elif info_char == "m" and (multipart_n or multipart_p):
            return PublicationType.multipart_monograph
        elif info_char == "m" and len(self.leader) >= SECOND_INFO_CHAR_I + 1:
            if self.leader[SECOND_INFO_CHAR_I] == "a":
                return PublicationType.multipart_monograph
            elif self.leader[SECOND_INFO_CHAR_I] == " ":
                return PublicationType.single_unit

        return PublicationType.monographic