def _ldtpize_accessible(self, acc):
        """
        Get LDTP format accessibile name

        @param acc: Accessible handle
        @type acc: object

        @return: object type, stripped object name (associated / direct),
                        associated label
        @rtype: tuple
        """
        actual_role = self._get_role(acc)
        label = self._get_title(acc)
        if re.match("AXWindow", actual_role, re.M | re.U | re.L):
            # Strip space and new line from window title
            strip = r"( |\n)"
        else:
            # Strip space, colon, dot, underscore and new line from
            # all other object types
            strip = r"( |:|\.|_|\n)"
        if label:
            # Return the role type (if, not in the know list of roles,
            # return ukn - unknown), strip the above characters from name
            # also return labely_by string
            label = re.sub(strip, u"", label)
        role = abbreviated_roles.get(actual_role, "ukn")
        if self._ldtp_debug and role == "ukn":
            print(actual_role, acc)
        return role, label