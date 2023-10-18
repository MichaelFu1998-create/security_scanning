def remove(self, id, operator="=", key=None):

        """ Deletes the row with given id.
        """

        if key == None: key = self._key
        try: id = unicode(id)
        except: pass        
        sql = "delete from "+self._name+" where "+key+" "+operator+" ?"
        self._db._cur.execute(sql, (id,))