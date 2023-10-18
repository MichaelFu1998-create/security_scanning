def get_member_list(self):
        """Return a list of direct members (_DAVResource or derived objects).

        This default implementation calls self.get_member_names() and
        self.get_member() for each of them.
        A provider COULD overwrite this for performance reasons.
        """
        if not self.is_collection:
            raise NotImplementedError
        memberList = []
        for name in self.get_member_names():
            member = self.get_member(name)
            assert member is not None
            memberList.append(member)
        return memberList