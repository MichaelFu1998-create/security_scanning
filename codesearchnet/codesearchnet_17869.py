def delete(self):
        """Delete a group and all associated memberships."""
        with db.session.begin_nested():
            Membership.query_by_group(self).delete()
            GroupAdmin.query_by_group(self).delete()
            GroupAdmin.query_by_admin(self).delete()
            db.session.delete(self)