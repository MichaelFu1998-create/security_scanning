def update_interfaces(self, added_sg, updated_sg, removed_sg):
        """Handles changes to interfaces' security groups

        Calls refresh_interfaces on argument VIFs. Set security groups on
        added_sg's VIFs. Unsets security groups on removed_sg's VIFs.
        """
        if not (added_sg or updated_sg or removed_sg):
            return

        with self.sessioned() as session:
            self._set_security_groups(session, added_sg)
            self._unset_security_groups(session, removed_sg)
            combined = added_sg + updated_sg + removed_sg
            self._refresh_interfaces(session, combined)