def get(self, key_name):
        """Return a dictionary consisting of the key itself

        e.g.
        {u'created_at': u'2016-10-10 08:31:53',
         u'description': None,
         u'metadata': None,
         u'modified_at': u'2016-10-10 08:31:53',
         u'name': u'aws',
         u'uid': u'459f12c0-f341-413e-9d7e-7410f912fb74',
         u'value': u'the_value'}

        """
        result = self.db.search(Query().name == key_name)
        if not result:
            return {}
        return result[0]