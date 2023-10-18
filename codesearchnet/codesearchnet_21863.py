def get_sqltext(self, format_=1):
        """retourne les requêtes actuellement lancées sur le serveur"""

        if format_ == 1:
            _sql = """SELECT u.sid, substr(u.username,1,12) user_name, s.sql_text
            FROM v$sql s,v$session u
            WHERE s.hash_value = u.sql_hash_value
            AND sql_text NOT LIKE '%from v$sql s, v$session u%'
            AND u.username NOT LIKE 'None'
            ORDER BY u.sid"""

        if format_ == 2:
            _sql = """SELECT u.username, s.first_load_time, s.executions, s.sql_text
            FROM dba_users u,v$sqlarea s
            WHERE u.user_id=s.parsing_user_id
            AND u.username LIKE 'LIONEL'
            AND sql_text NOT LIKE '%FROM dba_users u,v$sqlarea s%'
            ORDER BY s.first_load_time"""

        return psql.read_sql(_sql, self.conn)