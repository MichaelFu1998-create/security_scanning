def _connect(self):
        """
        Connexion à la base XAIR
        """

        try:
            # On passe par Oracle Instant Client avec le TNS ORA_FULL
            self.conn = cx_Oracle.connect(self._ORA_FULL)
            self.cursor = self.conn.cursor()
            print('XAIR: Connexion établie')
        except cx_Oracle.Error as e:
            print("Erreur: %s" % (e))
            raise cx_Oracle.Error('Echec de connexion')