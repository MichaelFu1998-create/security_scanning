def _remove_esc_chars(self, raw_message):
        """
        Removes any escape characters from the message
        :param raw_message: a list of bytes containing the un-processed data
        :return: a message that has the escaped characters appropriately un-escaped
        """
        message = []
        escape_next = False
        for c in raw_message:
            if escape_next:
                message.append(c ^ self._ESC_XOR)
                escape_next = False
            else:
                if c == self._ESC:
                    escape_next = True
                else:
                    message.append(c)

        return message