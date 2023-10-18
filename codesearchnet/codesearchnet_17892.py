def accept(self):
        """Activate membership."""
        with db.session.begin_nested():
            self.state = MembershipState.ACTIVE
            db.session.merge(self)