def add_parent(self, parent):
        """Add a parent to this role,
        and add role itself to the parent's children set.
        you should override this function if neccessary.

        Example::

            logged_user = RoleMixin('logged_user')
            student = RoleMixin('student')
            student.add_parent(logged_user)

        :param parent: Parent role to add in.
        """
        parent.children.add(self)
        self.parents.add(parent)